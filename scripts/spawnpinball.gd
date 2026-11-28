extends Node2D
var spawnball = preload('res://balls.tscn')


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if Input.is_action_just_pressed("spawnball"):
		var ball = spawnball.instantiate()
		ball.position = Vector2(764, 360)   # right of the chute (Lucas's circle)
		add_child(ball)	
		if ball.position < 680:
			queue_free()
