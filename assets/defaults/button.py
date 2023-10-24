class Button():
	def __init__(self, image1, pos, text_input, font, base_color, hovering_color, image2=None):
		"""
		Constructor de la clase Button.
		"""
		self.image1 = image1 # imagen normal
		self.image2 = image2 # imagen al pasar el mouse
		self.current_image = self.image1
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.current_image is None:
			self.current_image = self.text
		self.rect = self.current_image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		"""
		Método que actualiza el botón en la pantalla.
		"""
		if self.current_image is not None:
			screen.blit(self.current_image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		"""
		Método que verifica si el botón ha sido presionado.
		"""
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		"""
		Método que cambia el color del botón cuando el cursor está sobre él.
		"""
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
			if self.image2 is not None:
				self.current_image = self.image2
			return True
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
			self.current_image = self.image1
			return False