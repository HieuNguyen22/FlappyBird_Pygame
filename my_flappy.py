import pygame, sys, random 

## Ham 
# Ve san
def draw_floor():
	# Tạo 2 sàn liền nhau
	screen.blit(floor,(floor_x_pos,floor_y_pos)) 
	screen.blit(floor,(floor_x_pos + 576,floor_y_pos))

# Tao black hole
def create_black_hole():
	hole = black_hole.get_rect(center = (700,black_hole_y))
	return hole

# Di chuyen black hole
def move_black_hole(hole):  
	global visible_black_hole
	hole.centerx -= pipe_speed 	# Di chuyển sang trái nên trừ đi giá trị pipe_speed 
	if hole.right > -50 :
		visible_black_hole = hole		# Loại bỏ những ống đã ở ngoài màn hình
	return visible_black_hole 

# Tao ong  
def create_pipe():  
	random_pipe_pos = random.choice(pipe_height) 	# Random chiều cao ống trong list pipe_height đã tạo
	random_distance_pipe = random.randrange(300,350,50)		# Random khoảng cách 2 ống trên và dưới
	global black_hole_y 
	black_hole_y = random_pipe_pos - random_distance_pipe/2
	# Các image trong pygame k thể xác định vị trí, get_rect dùng để tạo 1 hcn bao quanh image để lấy được tọa độ
	bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))		
	top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - random_distance_pipe))
	return bottom_pipe,top_pipe

# Di chuyen ong
def move_pipes(pipes): 
	for pipe in pipes:
		# Di chuyển ống bằng cách thay đổi giá trị x của ống
		pipe.centerx -= pipe_speed 	# Di chuyển sang trái nên trừ đi giá trị pipe_speed 
	visible_pipes = [pipe for pipe in pipes if pipe.right > -50]	# Loại bỏ những ống đã ở ngoài màn hình
	return visible_pipes

# Ve ong
def draw_pipes(pipes):
	for pipe in pipes:
		# Kiểm tra nếu > chiều dài screen = 1024 thì là ống dưới, còn lại là ống trên
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)	# Ống trên sẽ xoay ngược lại sử dụng flip
			screen.blit(flip_pipe,pipe)
			
# Xu li va cham
def check_collision(pipes):
	global can_score
	for pipe in pipes:
		# Check va chạm ống
		if bird_rect.colliderect(pipe):		
			channel_death.play(death_sound)
			can_score = True
			return False

	# Check va chạm sàn và nóc màn hình
	if bird_rect.top <= -100 or bird_rect.bottom >= 900:
		channel_death.play(death_sound)
		can_score = True
		return False

	return True


# Xu li va cham voi ho den
def check_collision_black_hole(hole):
	if bird_rect.colliderect(hole):		
			channel_death.play(death_sound)
			black_hole.fill((0,0,0,0))	# Xoa black hole
			return True

	return False


# Xoay chim
def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
	return new_bird

# Chim dap canh
def bird_animation():
	# Hàm thay đổi trạng thái chim
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
	return new_bird,new_bird_rect

# Lightning animation
def lightning_animation():
	# Hàm thay đổi trạng thái sét
	new_lightning = lightning_frames[lightning_index]
	new_lightning_rect = new_lightning.get_rect(center = (100,bird_rect.centery-380))
	return new_lightning,new_lightning_rect

# Hien thi diem
def score_display(game_state):
	if game_state == 'main_game':	# Điểm tính khi đang chơi
		score_surface = game_font.render(str(int(score)),True,(255,255,255)) # Ép font
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':	# Điểm tính khi gameover
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255)) # Ép font
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

		# Điểm cao khi gameover
		high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

# Update highscore
def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

# Update score
def pipe_score_check():
	global score, can_score
	
	if pipe_list:
		for pipe in pipe_list:
			if 95 < pipe.centerx < 105 and can_score:
				score += 1
				channel_score.play(score_sound)
				can_score = False
			if pipe.centerx < 0:
				can_score = True



pygame.init()

# Dat kich thuoc man hinh
screen = pygame.display.set_mode((576,1024))
# FPS
clock = pygame.time.Clock()
# Dat font chu
game_font = pygame.font.Font('04B_19.ttf',40)

## Game Variables
# Dat trong luc
gravity = 0.25

# Bird di chuyen
bird_movement = 0

# Tinh diem
score = 0
high_score = 0
can_score = True

# Check thay doi
check_player = 0 	# Biến check người chơi
call_change_bg = 0
call_change_speed = 0

# Chen bg
bg = pygame.image.load('assets/background-day.png').convert()
bg = pygame.transform.scale2x(bg)

# Chen san
floor = pygame.image.load('assets/base.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
floor_y_pos = 900

# Tao chim
witch_cheems = 0 	# Bien check witch hay cheems
color_check = 3 	# Biến check màu
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())

# Tạo list các trạng thái của chim
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird = bird_frames[bird_index]
bird_rect = bird.get_rect(center = (100,512))

# Tao timer cho bird
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200) # Thời gian thay đổi trạng thái cho chim = 200ms

# Tao ong  
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [500,600,700] 
pipe_speed = 4 	# Biến hỗ trợ thay đổi tốc độ ống 

# Tao timer cho ong
SPAWNPIPE = pygame.USEREVENT
pipe_speed_time = 0 	# Biến thay đổi thời gian ra ống
pygame.time.set_timer(SPAWNPIPE,1300 - pipe_speed_time)

# Tao ho den
black_hole = pygame.image.load('assets/black_hole.png').convert_alpha()
black_hole = pygame.transform.scale(black_hole, (100, 100))
hole_adpapter = black_hole.get_rect(midtop = (1000,1000)) # Tạo biến ảo
black_hole_y = 0

# Tao lightning
checkLightning = 0  	# Biến check lightning
lightningBlank = pygame.image.load('assets/lightning/blank.png').convert_alpha()
lightning1 = pygame.transform.scale(pygame.image.load('assets/lightning/1.png').convert_alpha(),(400, 900))
lightning2 = pygame.transform.scale(pygame.image.load('assets/lightning/2.png').convert_alpha(),(400, 900))
lightning3 = pygame.transform.scale(pygame.image.load('assets/lightning/3.png').convert_alpha(),(400, 900))
lightning4 = pygame.transform.scale(pygame.image.load('assets/lightning/4.png').convert_alpha(),(400, 900))

# Tạo list trạng thái sét
lightning_frames = [lightningBlank,lightning1,lightning2,lightning3,lightning4]
lightning_index = 0
lightning = lightning_frames[lightning_index] 
lightning_rect = lightning.get_rect(center = (100,512))

# Tao timer cho lightning
LIGHTNINGPROCESS = pygame.USEREVENT + 1
pygame.time.set_timer(LIGHTNINGPROCESS,50) # Thời gian thay đổi trạng thái sét = 50ms

# Tao thunder
list_thunder = []
timer_thunder = pygame.USEREVENT
timer_draw = pygame.USEREVENT + 2
pygame.time.set_timer(timer_draw, 3000)
pygame.time.set_timer(timer_thunder, 1000)
thunder5 = pygame.image.load('assets/thunder5.png').convert_alpha()
thunder2 = pygame.image.load('assets/thunder2.png').convert_alpha() 
thunder1 = pygame.image.load('assets/thunder1.png').convert_alpha()
thunder6 = pygame.image.load('assets/thunder6.png').convert_alpha()
thunder7 = pygame.image.load('assets/thunder7.png').convert_alpha()
list_thunder.append(pygame.transform.scale(thunder2, (300, 500)))
list_thunder.append(pygame.transform.scale(thunder1, (300, 500)))
list_thunder.append(pygame.transform.scale(thunder5, (300, 500)))
list_thunder.append(pygame.transform.scale(thunder6, (300, 500)))
list_thunder.append(pygame.transform.scale(thunder7, (300, 500)))
thunder_mod = False
thunder_index = 0
thunder_x = 0

# Tao man hinh gameover
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

# Am thanh
bg_sound = pygame.mixer.Sound('sound/sfx_soundbg.wav')
bg_sound.set_volume(0.1)
thunder_sound = pygame.mixer.Sound('sound/sfx_thunder.mp3')		# Tiếng sấm
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')			# Tiếng đập cánh
death_sound = pygame.mixer.Sound('sound/sfx_fart.mp3')			# Tiếng ghi điểm
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')			# Tiếng chết
score_sound_countdown = 100
channel_bg = pygame.mixer.Channel(5) 		# channel nhac nen
channel_thunder = pygame.mixer.Channel(1) 
channel_flap = pygame.mixer.Channel(2)		# channel dap canh
channel_death = pygame.mixer.Channel(3)		# channel chet
channel_score = pygame.mixer.Channel(4)		# channel ghi diem

# Check game
game_active = False		# Biến check trạng thái game
check_black_hole = False  # Biến check vào hố đen
check_mode = 0
countdown_check_hole = 200



while True:
	bg_sound.play()
	# channel_bg.play(bg_sound)
	for event in pygame.event.get():

		# Check vao ho den
		if check_collision_black_hole(hole_adpapter):
			if countdown_check_hole == 200:
				countdown_check_hole -= 1
				check_black_hole = True
				if check_mode == 0:
					check_mode = 1
				elif check_mode == 1:
					check_mode = 0 
			elif countdown_check_hole == 0:
				countdown_check_hole = 200
			else:
				countdown_check_hole -= 1
		else:
			countdown_check_hole = 200

		# Ấn ESC hoặc Quit để thoát game
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			pygame.quit()
			sys.exit()

		# Bat su kien go phim 
		if event.type == pygame.KEYDOWN:
			# Phim space khi game dang chay
			if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and game_active:
				bird_movement = 0
				bird_movement -= 7  # Độ cao chim nhảy khi ấn Space
				channel_flap.play(flap_sound)
 

				print(check_black_hole)


			# Phim space khi game dung
			if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and game_active == False:
				game_active = True
				pipe_list.clear()				# Clear list ống
				bird_rect.center = (100,512)	# Đặt lại vị trí chim
				bird_movement = 0 				
				score = 0 						# Đặt lại điểm

			# Phim Enter: random mau
			if event.key == pygame.K_RETURN and game_active:
				if check_player == 0:	 
					# Doi mau
					color = [1,2,3] 
					color.remove(color_check)
					random_color = random.choice(color)
					if random_color == 1: 
						color_check = 1
						path = 'redbird'
					elif random_color == 2:
						color_check = 2
						path = 'yellowbird'
					elif random_color == 3:
						color_check = 3
						path = 'bluebird'
					bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/'+path+'-downflap.png').convert_alpha())
					bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/'+path+'-midflap.png').convert_alpha())
					bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/'+path+'-upflap.png').convert_alpha())
					bird_frames = [bird_downflap,bird_midflap,bird_upflap]

					# Lightning
					checkLightning = 1  	# Báo lightning
					channel_thunder.play(thunder_sound)

				elif check_player == 1:
					if witch_cheems == 0:
						witch_cheems = 1
						bird_downflap = pygame.transform.scale(pygame.image.load('assets/cheem.png').convert_alpha(),(55,55))
						bird_midflap = pygame.transform.scale(pygame.image.load('assets/cheem.png').convert_alpha(),(55,55))
						bird_upflap = pygame.transform.scale(pygame.image.load('assets/cheem.png').convert_alpha(),(55,55))
						bird_frames = [bird_downflap,bird_midflap,bird_upflap]
					else:
						witch_cheems = 0
						bird_downflap = pygame.transform.scale(pygame.image.load('assets/witch.png').convert_alpha(),(70,70))
						bird_midflap = pygame.transform.scale(pygame.image.load('assets/witch.png').convert_alpha(),(70,70))
						bird_upflap = pygame.transform.scale(pygame.image.load('assets/witch.png').convert_alpha(),(70,70))
						bird_frames = [bird_downflap,bird_midflap,bird_upflap]

					# Lightning
					checkLightning = 1  	# Báo lightning
					channel_thunder.play(thunder_sound)



			# # Check người chơi
			# if check_player == 0:
			# 	# Reset
			# 	call_change_bg = 0
			# 	call_change_speed = 0

			# 	# Check điểm để thay đổi background
			# 	call_change_bg = 1

			# 	# Check diem de tang toc
			# 	call_change_speed = 1

			# elif check_player == 1:
			# 	# Reset
			# 	call_change_bg = 0
			# 	call_change_speed = 0

			# 	# Check diem de tang toc
			# 	call_change_speed = 1


		# Dam vao ho den
		if check_black_hole and check_mode == 1:
			#Set lai check_black_hole
			check_black_hole = False

			# Set check player
			check_player = 1

			# Set witch
			bird_downflap = pygame.transform.scale(pygame.image.load('assets/witch.png').convert_alpha(),(70,70))
			bird_midflap = pygame.transform.scale(pygame.image.load('assets/witch.png').convert_alpha(),(70,70))
			bird_upflap = pygame.transform.scale(pygame.image.load('assets/witch.png').convert_alpha(),(70,70))
			bird_frames = [bird_downflap,bird_midflap,bird_upflap]

			# Lightning
			checkLightning = 1  	# Báo lightning
			channel_thunder.play(thunder_sound)

			# Set bg
			bg = pygame.image.load('assets/background-witch.jpg').convert()
			bg = pygame.transform.scale(bg,(700,1400))

			# Set ống
			pipe_surface = pygame.image.load('assets/pipe-witch.png').convert_alpha()
			pipe_surface = pygame.transform.scale(pipe_surface,(90,640))

			# Set sàn
			floor = pygame.image.load('assets/base-witch.png').convert_alpha()
			floor = pygame.transform.scale(floor,(772,300))
			floor_y_pos = 850

		elif check_black_hole and check_mode == 0:
			# Set witch or cheems
			witch_cheems == 0

			#Set lai check_black_hole
			check_black_hole = False
			
			# Set check player
			check_player = 0

			# Set lại bg
			bg = pygame.image.load('assets/background-day.png').convert()
			bg = pygame.transform.scale2x(bg)

			# Set lại ống
			pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
			pipe_surface = pygame.transform.scale2x(pipe_surface)

			# Set lại chim
			bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
			bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
			bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
			bird_frames = [bird_downflap,bird_midflap,bird_upflap]

			# Set lại sàn
			floor = pygame.image.load('assets/base.png').convert()
			floor = pygame.transform.scale2x(floor)
			floor_y_pos = 900

			# Lightning
			checkLightning = 1  	# Báo lightning
			channel_thunder.play(thunder_sound)

		# Check người chơi
		if check_player == 0:
			# Reset
			call_change_bg = 0
			call_change_speed = 0

			# Check điểm để thay đổi background
			call_change_bg = 1

			# Check diem de tang toc
			call_change_speed = 1

		elif check_player == 1:
			# Reset
			call_change_bg = 0
			call_change_speed = 0

			# Check diem de tang toc
			call_change_speed = 1

		# Tạo ống
		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		# Tao black hole
		if event.type == SPAWNPIPE:
			if score%2 == 0 and score != 0:
				black_hole = pygame.image.load('assets/black_hole.png').convert_alpha()
				black_hole = pygame.transform.scale(black_hole, (100, 100))
				hole_adpapter = create_black_hole()

		# Chim dap canh
		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird,bird_rect = bird_animation()

		# Lightning
		if checkLightning == 1:
			check = 0
			if event.type == LIGHTNINGPROCESS and check == 0:
				if lightning_index < 4:
					lightning_index += 1
				else:
					check = 1
					checkLightning = 0
					lightning_index = 0

				lightning,lightning_rect = lightning_animation()

		# Thunder	
		if event.type == timer_thunder:
		    thunder_index = random.randint(0, 4)
		    if thunder_mod:
		        thunder_mod = False
		    else:
		        thunder_mod = True
		    thunder_x = random.randint(-80, 300)
		if event.type == timer_draw:
		    if thunder_mod:
		        thunder_mod = False
		    thunder_x = random.randint(-80, 300)

		# Check diem de thay đổi bg
		if call_change_bg == 1 and game_active:
			if ((score/5)%2 == 0) and score != 0:		# Nếu điểm 20,40,60.. set background ngày
				bg = pygame.image.load('assets/background-day.png').convert()
				bg = pygame.transform.scale2x(bg)
			elif (score/5)%2 == 1 and game_active: 					# Nếu điểm 10,30,50.. set background đêm
				bg = pygame.image.load('assets/background-night.png').convert()
				bg = pygame.transform.scale2x(bg)


		# Check diem de thay doi speed
		if call_change_speed == 1 and game_active:
			if (score%5 == 0) and score != 0:			# Nếu điểm 10,20,30 thay đổi tốc độ game
				if score/5 != (pipe_speed - 4):		# Check ngoại lệ
					pipe_speed+=1
					pipe_speed_time += 400
					print(pipe_speed,"  ",pipe_speed_time)

			
	# Dat background
	screen.blit(bg,(0,0))


	if game_active:
		# Nhac nen
		# if score % 3 == 0:
		# 	bg_sound.play()

		# Thunder
		if check_player == 1:	
			if thunder_mod and timer_draw:
				screen.blit(list_thunder[thunder_index], (thunder_x, 0))

		# Lightning
		screen.blit(lightning,lightning_rect)

		# Bird di chuyen
		bird_movement += gravity
		rotated_bird = rotate_bird(bird)
		bird_rect.centery += bird_movement

		# Dat bird
		screen.blit(rotated_bird,bird_rect)

		# Move pipe 
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)

		# Move ho den
		hole_adpapter = move_black_hole(hole_adpapter)
		screen.blit(black_hole,hole_adpapter)

		# Check va cham
		game_active = check_collision(pipe_list)

		# Tinh diem
		pipe_score_check()
		score_display("main_game")
	else:
		# Tat nhac nen
		bg_sound.stop()

		# Set lai witch cheems 
		witch_cheems == 0

		# Set lai countdown_check_hole
		countdown_check_hole = 200

		# Set lai check_mode
		check_mode = 0

		# Xoa black hole
		# black_hole.fill((0,0,0,0))
		hole_adpapter = black_hole.get_rect(midtop = (1000,1000)) # Tạo biến ảo

		# Set lai check ho den
		check_black_hole = False

		# Set lai check player
		check_player = 0
		call_change_bg = 0
		call_change_speed = 0

		# Set màn hình gameover
		screen.blit(game_over_surface,game_over_rect) 
		high_score = update_score(score,high_score)

		# Set lại bg
		bg = pygame.image.load('assets/background-day.png').convert()
		bg = pygame.transform.scale2x(bg)

		# Set lại ống
		pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
		pipe_surface = pygame.transform.scale2x(pipe_surface)

		# Set lại chim
		bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
		bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
		bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
		bird_frames = [bird_downflap,bird_midflap,bird_upflap]

		# Set lại sàn
		floor = pygame.image.load('assets/base.png').convert()
		floor = pygame.transform.scale2x(floor)
		floor_y_pos = 900

		# Set lại speed
		pipe_speed = 4
		pipe_speed_time = 0

		score_display('game_over')

	# Dat san
	floor_x_pos -= 1
	draw_floor()

	# Loop san
	if floor_x_pos <= -576:
		floor_x_pos = 0


	pygame.display.update()
	clock.tick(120)