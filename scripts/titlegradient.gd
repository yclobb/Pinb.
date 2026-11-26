extends TextureRect
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	position.x = -1125.0
	modulate.a = 0.0
	var tween: 	Tween = create_tween().set_parallel(true)
	tween.tween_property(self, 'position:x', 0, 2.5).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(self, "modulate:a", 1.0, 3)
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
