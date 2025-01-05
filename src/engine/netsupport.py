from twisted.spread import pb
from src.engine import Light
from src.engine import Map
from src.engine import Unit
from src.engine import Ability
from src.engine import Class
from src.engine import Scenario
from src.engine import Range
from src.engine import Effect
from src.engine import Light
from src.engine import Equipment
from src.engine import Battle

pb.setUnjellyableForClass(Light.Light, Light.Light)
pb.setUnjellyableForClass(Map.MapSquare, Map.MapSquare)
pb.setUnjellyableForClass(Map.Map, Map.Map)
pb.setUnjellyableForClass(Unit.Unit, Unit.Unit)
pb.setUnjellyableForClass(Unit.StatusEffects, Unit.StatusEffects)
pb.setUnjellyableForClass(Ability.Ability, Ability.Ability)
pb.setUnjellyableForClass(Class.Class, Class.Class)
pb.setUnjellyableForClass(Scenario.Scenario, Scenario.Scenario)
pb.setUnjellyableForClass(Range.Line, Range.Line)
pb.setUnjellyableForClass(Range.Cross, Range.Cross)
pb.setUnjellyableForClass(Range.Diamond, Range.Diamond)
pb.setUnjellyableForClass(Range.DiamondExtend, Range.DiamondExtend)
pb.setUnjellyableForClass(Range.Single, Range.Single)

pb.setUnjellyableForClass(Effect.Damage, Effect.Damage)
pb.setUnjellyableForClass(Effect.DamageSP, Effect.DamageSP)
pb.setUnjellyableForClass(Effect.DrainLife, Effect.DrainLife)
pb.setUnjellyableForClass(Effect.HealFriendlyDamageHostile, Effect.HealFriendlyDamageHostile)
pb.setUnjellyableForClass(Effect.Healing, Effect.Healing)       
pb.setUnjellyableForClass(Effect.Status, Effect.Status)
pb.setUnjellyableForClass(Light.Light, Light.Light)
pb.setUnjellyableForClass(Light.White, Light.White)
pb.setUnjellyableForClass(Light.Point, Light.Point)
pb.setUnjellyableForClass(Light.Environment, Light.Environment)
pb.setUnjellyableForClass(Equipment.Weapon, Equipment.Weapon)
pb.setUnjellyableForClass(Equipment.Armor, Equipment.Armor)
pb.setUnjellyableForClass(Battle.Battle, Battle.Battle)
pb.setUnjellyableForClass(Battle.DefeatAllEnemies, Battle.DefeatAllEnemies)
pb.setUnjellyableForClass(Battle.PlayerDefeated, Battle.PlayerDefeated)
pb.setUnjellyableForClass(Effect.MissResult, Effect.MissResult)
pb.setUnjellyableForClass(Effect.DamageResult, Effect.DamageResult)
pb.setUnjellyableForClass(Effect.DamageSPResult, Effect.DamageSPResult)
pb.setUnjellyableForClass(Effect.HealResult, Effect.HealResult)
pb.setUnjellyableForClass(Effect.StatusResult, Effect.StatusResult)


