from twisted.spread import pb
from engine import Light
from engine import Map
from engine import Unit
from engine import Ability
from engine import Class
from engine import Scenario
from engine import Range
from engine import Effect
from engine import Light
from engine import Equipment
from engine import Battle

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


