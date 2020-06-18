class Weapon:
    def __init__(self, name, damage):
        """武器基础属性"""
        self.name=name
        self.damage=damage
        
    def take_weapon(self, hro):
        """将武器给予英雄，英雄攻击力提升"""
        print("将武器{}装备给英雄{}".format(self.name, hro.name))
        hro.damage+=self.damage
        print("{}的攻击力变为{}".format(hro.name, hro.damage))
