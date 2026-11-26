extends Node2D
## Sketch table. A = everything on the left (flipper + boosters), D = everything on the right.

@export var flip_angle_deg: float = 45.0   ## how far flippers swing up
@export var flip_speed: float = 18.0       ## radians per second
@export var windmill_speed: float = 0.8    ## radians per second (slow flap)
@export var kick_strength: float = 900.0   ## speed a booster gives the ball
@export var launch_speed: float = 1250.0   ## how hard the ball is shot up the entry lane
@export var launch_tilt_deg: float = 6.0  ## tilt left so the ball rides the top wall instead of bouncing back
@export var ball_radius: float = 8.5       ## smaller than the main game's ball so it fits the sketch's gaps
@export var drain_y: float = 700.0         ## ball below this is re-launched

var ball_scene: PackedScene = preload("res://balls.tscn")
var spawn: Vector2
var ball: RigidBody2D


func _ready() -> void:
	spawn = $Ball.position
	$Ball.queue_free()
	_launch()


func _physics_process(delta: float) -> void:
	var left := Input.is_key_pressed(KEY_A)
	var right := Input.is_key_pressed(KEY_D)
	_flip($FlipperL, left, -1.0, delta)
	_flip($FlipperR, right, 1.0, delta)
	if Input.is_key_pressed(KEY_A) and not _was_left: _fire("left")
	if Input.is_key_pressed(KEY_D) and not _was_right: _fire("right")
	_was_left = left
	_was_right = right
	$Windmill.rotation += windmill_speed * delta
	if ball.global_position.y > drain_y:
		ball.queue_free()
		_launch()

var _was_left := false
var _was_right := false


func _flip(f: Node2D, up: bool, dir: float, delta: float) -> void:
	var target: float = dir * deg_to_rad(flip_angle_deg) if up else 0.0
	f.rotation = move_toward(f.rotation, target, flip_speed * delta)


func _fire(side: String) -> void:
	# a booster only kicks if the ball is touching it when you press
	for k in get_tree().get_nodes_in_group("kickers"):
		if k.get_meta("side") == side and ball in k.get_node("Area").get_overlapping_bodies():
			ball.linear_velocity = (k.get_meta("kick_dir") as Vector2).normalized() * kick_strength


func _launch() -> void:
	ball = ball_scene.instantiate()
	ball.position = spawn
	var shape: CircleShape2D = ball.get_node("CollisionShape2D").shape.duplicate()
	var old_r: float = shape.radius
	shape.radius = ball_radius
	ball.get_node("CollisionShape2D").shape = shape
	ball.get_node("Sprite2D").scale *= ball_radius / old_r
	ball.linear_velocity = Vector2(0, -launch_speed).rotated(-deg_to_rad(launch_tilt_deg))
	add_child(ball)
