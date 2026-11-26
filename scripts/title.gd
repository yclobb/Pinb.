extends RichTextLabel


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	bbcode_enabled = true
	fit_content = true
	add_theme_font_override("normal_font", load("res://fonts/Anton.ttf"))
	text = "[center][font_size=140]Pinb[/font_size]\n[font_size=25]   A MX STUDIOS PRODUCTION[/font_size][/center]"


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
