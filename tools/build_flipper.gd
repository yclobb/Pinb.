# Builds res://flipper.tscn from art/parts/flipper.png (+ its body mask for collision).
extends SceneTree
func _initialize() -> void:
	var bm := BitMap.new()
	bm.create_from_image_alpha(Image.load_from_file(ProjectSettings.globalize_path("res://art/parts/flipper.png")), 0.92)
	var polys := bm.opaque_to_polygons(Rect2i(Vector2i.ZERO, bm.get_size()), 6.0)
	var best: PackedVector2Array
	for p in polys:
		if p.size() > best.size(): best = p
	var rel := PackedVector2Array()
	for p in best: rel.append(p - Vector2(245, 331))
	var root_node := AnimatableBody2D.new(); root_node.name = "Flipper"
	root_node.set_script(load("res://scripts/flipper.gd"))
	var art := Sprite2D.new(); art.name = "Art"; art.texture = load("res://art/parts/flipper.png")
	root_node.add_child(art); art.owner = root_node
	var col := CollisionPolygon2D.new(); col.name = "Shape"; col.polygon = rel
	root_node.add_child(col); col.owner = root_node
	var ps := PackedScene.new(); ps.pack(root_node)
	print("BUILD flipper points=", rel.size(), " save=", ResourceSaver.save(ps, "res://flipper.tscn"))
	root_node.free(); quit()
