class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		self.clicked = False

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

	def draw(self, surface, mouse_pos, mouseGetPressed):
		action = False

		#get mouse position
		pos = mouse_pos

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if mouseGetPressed[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if mouseGetPressed[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
	
	def drag(self, surface, mouse_pos, mouse_get_pressed):
		action = False
		pos = mouse_pos

		if self.rect.collidepoint(pos):
			if mouse_get_pressed[0] == 1:
				action = True
		
		return action