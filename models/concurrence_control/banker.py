import numpy as np
from threading import Lock

class Banker:
    def __init__(self, total_resources: dict, max_demand: dict):
        self.lock = Lock()
        self.total_resources = total_resources  # {'lab': 3, 'tool_1': 2, 'tool_2': 3, ...}
        print(f"[INIT] Recursos totales: {self.total_resources}")
        self.available = total_resources.copy()
        self.max_demand = max_demand  # {student_id: {'lab': 1, 'tool_1': 1, 'tool_2': 2}}
        print(f"[INIT] Demanda máxima: {self.max_demand}")
        self.allocation = {sid: {r: 0 for r in total_resources} for sid in max_demand}
        print(f"[INIT] Asignación inicial: {self.allocation}")
        self.need = {
            sid: {r: max_demand[sid][r] for r in max_demand[sid]}
            for sid in max_demand
        }
        print(f"[INIT] Necesidad inicial: {self.need}")

    def is_safe(self, sid, request):
        print(f"\n[SAFE] Proceso {sid} solicita: {request}")
        print(f"[SAFE] Estado disponible antes de simulación: {self.available}")
        print(f"[SAFE] Necesidad antes de simulación: {self.need[sid]}")
        # Paso 1: Comprobar que la solicitud no excede lo que necesita
        for r in request:
            if request[r] > self.need[sid][r]:
                print(f"[SAFE][ERROR] Solicitud de {r} excede la necesidad ({request[r]} > {self.need[sid][r]})")
                return False
            
        # Paso 2: Comprobar que los recursos están disponibles
        for r in request:
            if request[r] > self.available[r]:
                print(f"[SAFE][ERROR] Solicitud de {r} excede lo disponible ({request[r]} > {self.available[r]})")
                return False

        # Paso 3: Simular asignación temporal
        work = self.available.copy()
        temp_allocation = {k: v.copy() for k, v in self.allocation.items()}
        temp_need = {k: v.copy() for k, v in self.need.items()}

        for r in request:
            work[r] -= request[r]
            temp_allocation[sid][r] += request[r]
            temp_need[sid][r] -= request[r]
        print(f"[SAFE] Estado simulado tras asignación:")
        print(f"        work: {work}")
        print(f"        temp_allocation: {temp_allocation}")
        print(f"        temp_need: {temp_need}")

        finish = {k: False for k in self.allocation}
        print(f"[SAFE] Estado inicial de finish: {finish}")

        while True:
            found = False
            for pid in finish:
                if not finish[pid] and all(temp_need[pid][r] <= work[r] for r in work):
                    print(f"[SAFE] Proceso {pid} puede finalizar. work antes: {work}")
                    for r in work:
                        work[r] += temp_allocation[pid][r]
                    finish[pid] = True
                    found = True
                    print(f"[SAFE] Proceso {pid} marcado como terminado. work después: {work}")
            if not found:
                break
        print(f"[SAFE] Estado final de finish: {finish}")
        seguro = all(finish.values())
        print(f"[SAFE] ¿Estado seguro?: {seguro}")
        return seguro

    def request_resources(self, sid, request):
        print(f"\n[REQUEST] Proceso {sid} solicita recursos: {request}")
        with self.lock:
            if not self.is_safe(sid, request):
                print(f"[REQUEST][DENEGADO] Solicitud NO segura para {sid}.")
                return False  # Estado no seguro
            print(f"[REQUEST][APROBADO] Solicitud segura. Asignando recursos a {sid}.")
            for r in request:
                self.available[r] -= request[r]
                self.allocation[sid][r] += request[r]
                self.need[sid][r] -= request[r]
            print(f"[REQUEST] Estado tras asignación:")
            print(f"          available: {self.available}")
            print(f"          allocation: {self.allocation}")
            print(f"          need: {self.need}")
            return True

    def release_resources(self, sid):
        print(f"\n[RELEASE] Proceso {sid} libera todos sus recursos.")
        with self.lock:
            for r in self.total_resources:
                print(f"[RELEASE] Liberando {self.allocation[sid][r]} de {r} de {sid}")
                self.available[r] += self.allocation[sid][r]
                self.allocation[sid][r] = 0
                self.need[sid][r] = self.max_demand[sid][r]
            print(f"[RELEASE] Estado tras liberar:")
            print(f"           available: {self.available}")
            print(f"           allocation: {self.allocation}")
            print(f"           need: {self.need}")