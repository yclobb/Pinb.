extends AnimatableBody2D
@export var hitrange = 50.0
@export var fliptime = 0.09
@export var fdirection = "leftflipper" #set to rightflipper if faste right obv
var flipping = false
var tween: Tween
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _physics_process(delta: float) -> void:
	if flipping == false:
		if Input.is_action_pressed("upflipper"):   # one key flips both; fdirection still says which side this flipper is
			flipping = true
			if fdirection == "leftflipper":
				swing(-deg_to_rad(hitrange))
			elif fdirection == 'rightflipper':
				swing(+deg_to_rad(hitrange))
	else:
		if not Input.is_action_pressed("upflipper"):
			flipping = false
			swing(0.0)
func swing(target: float) -> void:
	if tween:
		tween.kill()
	var time = fliptime * abs(target - rotation) / deg_to_rad(hitrange)
	tween = create_tween()
	tween.set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)
	tween.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(self, 'rotation', target, time)
