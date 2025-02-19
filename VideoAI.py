from manim import *
from pydub import AudioSegment

AudioSegment.converter = r"D:\BIT n BUILD\pythonProject\animatedPodcast\animatedPodcast\External Requirements\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"D:\BIT n BUILD\pythonProject\animatedPodcast\animatedPodcast\External Requirements\ffmpeg-7.1-essentials_build\bin\ffprobe.exe"

class CircleHost(VGroup):
    def __init__(self, position=ORIGIN, face_color=WHITE, feature_color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.feature_color = feature_color
        self.talking = False

        self.face = Circle(radius=1, color=face_color, fill_color=face_color, fill_opacity=1).move_to(position)
        self.mouth = VMobject()
        self.set_idle_mouth()
        self.mouth.add_updater(lambda mob, dt: self.update_mouth(dt))

        self.radial_wave = VGroup()
        self.radial_wave.add_updater(lambda mob, dt: self.update_radial_wave(mob, dt))

        self.left_eye, self.right_eye, self.left_eyebrow, self.right_eyebrow = self.create_eyes_and_eyebrows(self.face.get_center())

        self.add(self.face, self.radial_wave, self.mouth, self.left_eye, self.right_eye, self.left_eyebrow, self.right_eyebrow)

    def set_idle_mouth(self):
        center = self.face.get_center()
        left_corner, right_corner = center + LEFT * 0.3 + UP * 0.2, center + RIGHT * 0.3 + UP * 0.2
        control_point = (left_corner + right_corner) / 2 + DOWN * 0.15
        points = [(1 - s)**2 * left_corner + 2 * (1 - s) * s * control_point + s**2 * right_corner for s in np.linspace(0, 1, 20)]
        self.mouth.become(VMobject().set_points_as_corners(points).set_stroke(color=self.feature_color, width=9))

    def update_mouth(self, dt):
        if self.talking:
            center = self.face.get_center()
            left_corner, right_corner = center + LEFT * 0.3 + UP * 0.2, center + RIGHT * 0.3 + UP * 0.2
            control_point = (left_corner + right_corner) / 2 + DOWN * (0.15 + 0.12 * self.get_amp(self.current_time) * np.sin(self.current_time * 10))
            points = [(1 - s)**2 * left_corner + 2 * (1 - s) * s * control_point + s**2 * right_corner for s in np.linspace(0, 1, 20)]
            self.mouth.become(VMobject().set_points_as_corners(points).set_stroke(color=self.feature_color, width=9))
        else:
            self.set_idle_mouth()

    def update_radial_wave(self, mob, dt):
        num_sectors = 20
        base_extension = 0.2
        amp = 1.0 * (self.get_amp(self.current_time) * 0.5 * (np.sin(self.current_time * 10) + 1)) if self.talking else 0
        new_group = VGroup()
        for i in range(num_sectors):
            new_group.add(AnnularSector(inner_radius=1, outer_radius=1 + base_extension + amp, start_angle=i * TAU / num_sectors, angle=TAU / num_sectors * 0.8, color=self.feature_color, fill_opacity=0.7, stroke_width=0))
        mob.become(new_group).move_to(self.face.get_center())

    def create_eyes_and_eyebrows(self, position):
        eye_radius = 0.15
        pupil_radius = 0.07
        left_eye_center = position + LEFT * 0.3 + UP * 0.3
        right_eye_center = position + RIGHT * 0.3 + UP * 0.3

        left_eye = Circle(radius=eye_radius, color=BLACK, fill_color=WHITE, fill_opacity=1)
        right_eye = Circle(radius=eye_radius, color=BLACK, fill_color=WHITE, fill_opacity=1)
        left_eye.move_to(left_eye_center)
        right_eye.move_to(right_eye_center)

        look_dir = RIGHT if position[0] < 0 else LEFT
        pupil_offset = look_dir * 0.05
        left_pupil = Circle(radius=pupil_radius, color=BLACK, fill_color=BLACK, fill_opacity=1)
        right_pupil = Circle(radius=pupil_radius, color=BLACK, fill_color=BLACK, fill_opacity=1)
        left_pupil.move_to(left_eye.get_center() + pupil_offset)
        right_pupil.move_to(right_eye.get_center() + pupil_offset)
        left_eye.add(left_pupil)
        right_eye.add(right_pupil)

        eyebrow_offset_up = UP * 0.20
        eyebrow_offset_side = 0.1
        left_eyebrow_start = left_eye_center + LEFT * eyebrow_offset_side + eyebrow_offset_up
        left_eyebrow_end = left_eye_center + RIGHT * eyebrow_offset_side + eyebrow_offset_up
        left_eyebrow = Line(left_eyebrow_start, left_eyebrow_end,
                            color=self.feature_color, stroke_width=4)
        right_eyebrow_start = right_eye_center + LEFT * eyebrow_offset_side + eyebrow_offset_up
        right_eyebrow_end = right_eye_center + RIGHT * eyebrow_offset_side + eyebrow_offset_up
        right_eyebrow = Line(right_eyebrow_start, right_eyebrow_end,
                             color=self.feature_color, stroke_width=4)
        return left_eye, right_eye, left_eyebrow, right_eyebrow

    get_amp = staticmethod(lambda t: 0)

class TalkingCharacters(MovingCameraScene):
    def construct(self, background_path="Images/Background1.jpeg"):
        background = ImageMobject(background_path).scale_to_fit_width(config.frame_width).to_edge(DOWN)
        self.add(background)

        with open("sample.csv", "r") as f:
            segments_host, segments_guest = [], []
            for line in f.readlines()[1:]:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    start, duration, speaker = float(parts[0]), float(parts[1]), parts[2].strip()
                    if speaker == "SPEAKER_01": segments_host.append((start, start + duration))
                    elif speaker == "SPEAKER_00": segments_guest.append((start, start + duration))

        audio_seg, sample_interval = AudioSegment.from_mp3("audio/sample.wav"), 50
        amp_array = [audio_seg[i * sample_interval:(i + 1) * sample_interval].rms for i in range(len(audio_seg) // sample_interval)]
        max_amp = max(amp_array) or 1
        amp_array = [amp / max_amp for amp in amp_array]
        CircleHost.get_amp = staticmethod(lambda t: amp_array[int(t * 1000 / sample_interval)] if int(t * 1000 / sample_interval) < len(amp_array) else 0)

        host, guest = CircleHost(LEFT * 4, WHITE, PURPLE), CircleHost(RIGHT * 4, WHITE, TEAL)
        self.add(host, guest)

        self.add_updater(lambda dt: [setattr(m, "current_time", self.renderer.time) for m in [host, guest]])
        host.add_updater(lambda m, dt: setattr(m, "talking", any(start <= self.renderer.time < end for start, end in segments_guest)))
        guest.add_updater(lambda m, dt: setattr(m, "talking", any(start <= self.renderer.time < end for start, end in segments_host)))

        self.wait(max([end for _, end in segments_host + segments_guest], default=10))
        host.clear_updaters()
        guest.clear_updaters()
