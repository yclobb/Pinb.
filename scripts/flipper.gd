extends AnimatableBody2D
## One flipper. Rotate THIS node to flip (rotation 0 = resting). Mirror with right_side.

@export var right_side: bool = false
@export var rest_deg: float = 30.0      ## resting angle, pointing down toward the centre
@export var length_px: float = 48.0     ## pivot-to-tip length in game pixels (mods can change this)

const ART_PIVOT := Vector2(245, 331)    ## pin centre in flipper.png
const ART_LENGTH := 1434.0              ## pin-to-tip length in flipper.png
const ART_ANGLE_DEG := 3.7              ## the art itself leans down this much


func _ready() -> void:
	var s: float = length_px / ART_LENGTH
	var rot: float = deg_to_rad(rest_deg - ART_ANGLE_DEG)
	var side: float = -1.0 if right_side else 1.0
	var art: Sprite2D = $Art
	art.centered = false
	art.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS   # smooth when shrunk to game size
	art.offset = -ART_PIVOT
	art.scale = Vector2(s * side, s)
	art.rotation = rot * side
	var col: CollisionPolygon2D = $Shape
	var pts := PackedVector2Array()
	for p in col.polygon:   # polygon is stored in art pixels relative to the pin
		pts.append((Vector2(p.x * side, p.y) * s).rotated(rot * side))
	col.polygon = pts
