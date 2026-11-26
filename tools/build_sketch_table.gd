# Builds res://sketch_table.tscn from art/sketch/walls.png + pieces.png and makes it playable.
# Run: Godot --headless --path . -s tools/build_sketch_table.gd
extends SceneTree
const REGION := Rect2i(215, 50, 400, 600)
const S := 1.06
const MID := Vector2(415, 50)
# piece role by where it sits in the sketch (sketch px). kick = direction of the arrow Lucas drew next to it.
const ROLES := {
	"KickerTL": {"at": Vector2(340, 240), "kick": Vector2(0.5, -0.87)},
	"FinL": {"at": Vector2(393, 335)},
	"FinR": {"at": Vector2(495, 363)},
	"Windmill": {"at": Vector2(430, 378)},
	"KickerL": {"at": Vector2(305, 494), "kick": Vector2(0.8, -0.6)},
	"KickerR": {"at": Vector2(540, 563), "kick": Vector2(-0.85, -0.5)},
	"FlipperL": {"at": Vector2(408, 622)},
	"FlipperR": {"at": Vector2(474, 622)},
}
var root_node: Node2D
var bounce := PhysicsMaterial.new()
func to_game(p: Vector2) -> Vector2:
	return (p - MID) * S + Vector2(576, 2)
func traced(path: String) -> Array:
	var bm := BitMap.new()
	bm.create_from_image_alpha(Image.load_from_file(ProjectSettings.globalize_path(path)), 0.5)
	var out := []
	for poly in bm.opaque_to_polygons(REGION, 1.0):
		var pts := PackedVector2Array()
		for p in poly:
			pts.append(p + Vector2(REGION.position))   # sketch coordinates
		out.append(pts)
	return out
func centroid(pts: PackedVector2Array) -> Vector2:
	var c := Vector2.ZERO
	for p in pts: c += p
	return c / pts.size()
func own(n: Node, parent: Node) -> Node:
	parent.add_child(n); n.owner = root_node; return n
func shape(parent: Node, pts_game: PackedVector2Array, colour: Color, nm: String) -> void:
	var col := CollisionPolygon2D.new(); col.name = nm; col.polygon = pts_game; own(col, parent)
	var vis := Polygon2D.new(); vis.name = nm + "Art"; vis.polygon = pts_game; vis.color = colour; own(vis, parent)
func local(pts: PackedVector2Array, origin: Vector2) -> PackedVector2Array:
	var o := PackedVector2Array()
	for p in pts: o.append(to_game(p) - origin)
	return o
func _initialize() -> void:
	bounce.bounce = 0.3
	root_node = Node2D.new(); root_node.name = "SketchTable"
	root_node.set_script(load("res://scripts/sketch_table.gd"))
	var bg := ColorRect.new(); bg.name = "Background"; bg.size = Vector2(1152, 648); bg.color = Color(0.07, 0.13, 0.2)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE; own(bg, root_node)
	var walls := StaticBody2D.new(); walls.name = "Walls"; walls.physics_material_override = bounce; own(walls, root_node)
	var i := 0
	for pts in traced("res://art/sketch/walls.png"):
		shape(walls, local(pts, Vector2.ZERO), Color(0.85, 0.9, 1.0), "Wall%d" % i); i += 1
	var orange := Color(1.0, 0.45, 0.1)
	for pts in traced("res://art/sketch/pieces.png"):
		var c := centroid(pts)
		var role := ""
		var best := INF
		for r in ROLES:
			var d: float = c.distance_to(ROLES[r]["at"])
			if d < best: best = d; role = r
		if role.begins_with("Fin"):
			shape(walls, local(pts, Vector2.ZERO), orange, role)
		elif role == "Windmill":
			var moved := PackedVector2Array()
			var dest := Vector2(345, 565)   # empty space above the pit of doom (Lucas)
			for p in pts: moved.append(p - c + dest)
			var w := AnimatableBody2D.new(); w.name = role; w.position = to_game(dest); own(w, root_node)
			shape(w, local(moved, w.position), orange, "Flap")
		elif role.begins_with("Flipper"):
			# pivot = the round outer end: leftmost point for the left flipper, rightmost for the right
			var piv: Vector2 = pts[0]
			for p in pts:
				if (role == "FlipperL" and p.x < piv.x) or (role == "FlipperR" and p.x > piv.x): piv = p
			piv += Vector2(6, 2) if role == "FlipperL" else Vector2(-6, 2)
			var short := PackedVector2Array()
			for p in pts: short.append(piv + (p - piv) * 0.8)   # shorter blades: wider drop between flippers (Lucas)
			pts = short
			var f: Node2D = load("res://flipper.tscn").instantiate(); f.name = role; f.position = to_game(piv)
			f.right_side = role == "FlipperR"; f.rest_deg = 35.0; f.length_px = 48.0
			f.physics_material_override = bounce
			own(f, root_node)
		else:   # kicker
			var shrunk := PackedVector2Array()
			for p in pts: shrunk.append(c + (p - c) * 0.75)   # boosters drawn smaller (Lucas)
			pts = shrunk
			var k := StaticBody2D.new(); k.name = role; k.add_to_group("kickers", true)
			k.set_meta("side", "left" if c.x < 430.0 else "right")
			k.set_meta("kick_dir", ROLES[role]["kick"]); own(k, root_node)
			shape(k, local(pts, Vector2.ZERO), Color(1.0, 0.3, 0.15), "Body")
			var a := Area2D.new(); a.name = "Area"; own(a, k)
			var grown := PackedVector2Array()
			var cg := to_game(c)
			for p in local(pts, Vector2.ZERO): grown.append(cg + (p - cg) * 1.18)   # slightly bigger: touching = kick
			var ac := CollisionPolygon2D.new(); ac.name = "Touch"; ac.polygon = grown; own(ac, a)
		print("PIECE ", role, " at ", c.round())
	var ball: Node = load("res://balls.tscn").instantiate(); ball.name = "Ball"
	ball.position = to_game(Vector2(534, 372)); own(ball, root_node)   # bottom of the entry lane
	var ps := PackedScene.new(); ps.pack(root_node)
	print("BUILD save_err=", ResourceSaver.save(ps, "res://sketch_table.tscn"))
	root_node.free(); quit()
