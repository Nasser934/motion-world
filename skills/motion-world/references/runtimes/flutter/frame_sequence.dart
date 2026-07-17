import 'motion_progress.dart';

class FrameSequence {
  static int index(double progress, int frameCount, {bool reducedMotion = false}) {
    final count = frameCount < 1 ? 1 : frameCount;
    var p = MotionProgress.clamp(progress);
    if (reducedMotion) p = p < 0.25 ? 0 : (p < 0.75 ? 0.5 : 1);
    return (p * (count - 1)).round().clamp(0, count - 1);
  }

  static String fileName(double progress, int frameCount, {bool reducedMotion = false}) {
    final i = index(progress, frameCount, reducedMotion: reducedMotion);
    return 'frame_${i.toString().padLeft(4, '0')}.webp';
  }
}
