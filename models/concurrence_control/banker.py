import numpy as np
from threading import Lock

class Banker:
    def __init__(self, total_resources: dict, max_demand: dict):
        self.lock = Lock()
        self.total_resources = total_resources  # {'lab': 3, 'tool_1': 2, 'tool_2': 3, ...}
        #print(f"[DEBUG][BANK] Total resources: {self.total_resources}")
        self.available = total_resources.copy()
        self.max_demand = max_demand  # {student_id: {'lab': 1, 'tool_1': 1, 'tool_2': 2}}
        #print(f"[DEBUG][BANK] Max demand: {self.max_demand}")
        # crea una estructura inicial vacía que representa como se asignan los recursos
        # a cada estudiante (sid) para cada recurso (r)
        # {'sid1': {'lab': 0, 'tool_1': 0, 'tool_2': 0, ...}, 'sid2': {...}, ...}
        self.allocation = {sid: {r: 0 for r in total_resources} for sid in max_demand}
        #representa lo que cada usuario aún puede pedir de cada recurso. Al inicio, es igual a 
        # la demanda máxima, y se va reduciendo a medida que se asignan recursos.
        self.need = {
            sid: {r: max_demand[sid][r] for r in max_demand[sid]}
            for sid in max_demand
        }

    def is_safe(self, sid, request):
        """
        Simula el préstamo temporal de recursos y verifica si el sistema se mantiene en un estado seguro.
        """
        # Paso 1: Comprobar que la solicitud no excede lo que necesita
        for r in request:
            if request[r] > self.need[sid][r]:
                return False
            
        # Paso 2: Comprobar que los recursos están disponibles
        for r in request:
            if request[r] > self.available[r]:
                return False

        # Paso 3: Simular asignación temporal
        work = self.available.copy()
        temp_allocation = {k: v.copy() for k, v in self.allocation.items()}
        #print(f"[DEBUG][BANK] temp_allocation: {temp_allocation}")
        temp_need = {k: v.copy() for k, v in self.need.items()}
        #print(f"[DEBUG][BANK] temp_need: {temp_need}")

        for r in request:
            #Resta la cantidad solicitada de ese recurso a los recursos disponibles simulados
            work[r] -= request[r]
            #print(f"[DEBUG][BANK] Work after request {r}: {work}")
            #Simula que el proceso tiene ahora esos recursos asignados.
            temp_allocation[sid][r] += request[r]
            #print(f"[DEBUG][BANK] Temp allocation after request {r}: {temp_allocation[sid]}")
            #Simula que el proceso necesita menos recursos porque ya se le asignaron algunos.
            temp_need[sid][r] -= request[r]
            #print(f"[DEBUG][BANK] Temp need after request {r}: {temp_need[sid]}")

        finish = {k: False for k in self.allocation}
        #print(f"[DEBUG][BANK] Initial finish state: {finish}")

        while True:
            found = False
            for pid in finish:
                # Recorre todos los recursos, Para cada recurso, compara la necesidad pendiente 
                # de ese proceso (temp_need[pid][r]) con la cantidad de ese recurso disponible 
                # en el sistema simulado (work[r]).
                if not finish[pid] and all(temp_need[pid][r] <= work[r] for r in work):
                    
                    for r in work:
                        work[r] += temp_allocation[pid][r]
                    finish[pid] = True
                    found = True
            if not found:
                break
        #print(f"[DEBUG][BANK] Final finish state: {finish}")        
        return all(finish.values())

    def request_resources(self, sid, request):
        """Aplica el algoritmo del banquero de forma segura con lock."""
        with self.lock:
            if not self.is_safe(sid, request):
                return False  # Estado no seguro
            # 2. Si es seguro, asigna los recursos solicitados al proceso.
            for r in request:
                self.available[r] -= request[r]         # Resta los recursos disponibles.
                self.allocation[sid][r] += request[r]   # Suma los recursos asignados al proceso.
                self.need[sid][r] -= request[r]         # Disminuye la necesidad pendiente del proceso.
            return True

    def release_resources(self, sid):
        """Libera todos los recursos del proceso (cuando termina la reserva)."""
        with self.lock:
            for r in self.total_resources:
                self.available[r] += self.allocation[sid][r]
                self.allocation[sid][r] = 0
                self.need[sid][r] = self.max_demand[sid][r]