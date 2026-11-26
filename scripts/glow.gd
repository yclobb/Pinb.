extends Control


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	await get_tree().create_timer(2.5).timeout
	modulate.a = 0.5
	await get_tree().create_timer(0.15).timeout
	modulate.a = 0.3
	await get_tree().create_timer(0.1).timeout
	modulate.a = 0.7
	await get_tree().create_timer(0.1).timeout
	modulate.a = 0.4
	await get_tree().create_timer(0.1).timeout
	modulate.a = 0.8
	await get_tree().create_timer(0.2).timeout
	modulate.a = 0.3
	await get_tree().create_timer(0.25).timeout
	modulate.a = 1.0
	await get_tree().create_timer(0.15).timeout
	modulate.a = 0.5
	await get_tree().create_timer(0.1).timeout
	modulate.a = 1.0
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
