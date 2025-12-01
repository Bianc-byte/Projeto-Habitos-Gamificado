class Avatar:
    def __init__(self):
        self.xp = 0
        self.nivel = 1
        self.estado = "iniciante"

    def adicionar_xp(self, valor):
        self.xp += valor

        while self.xp >= self.nivel * 100:
            self.xp -= self.nivel * 100
            self.nivel += 1
            self.atualizar_estado()

    def atualizar_estado(self):
        if self.nivel < 5:
            self.estado = "iniciante"
        elif 5 <= self.nivel <= 10:
            self.estado = "intermediário"
        else:
            self.estado = "avançado"

    def __repr__(self):
        return f"Avatar(nível={self.nivel}, xp={self.xp}, estado='{self.estado}')"
