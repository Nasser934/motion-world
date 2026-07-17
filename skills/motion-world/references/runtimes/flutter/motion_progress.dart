class MotionProgress {
  static double clamp(double value) {
    if (!value.isFinite) return 0;
    return value.clamp(0.0, 1.0);
  }

  static double elapsed(DateTime now, DateTime start, DateTime end) {
    final duration = end.difference(start).inMilliseconds;
    if (duration <= 0) return now.isAfter(end) || now == end ? 1 : 0;
    return clamp(now.difference(start).inMilliseconds / duration);
  }

  static double countdown(double remaining, double total) {
    if (total <= 0) return remaining <= 0 ? 1 : 0;
    return clamp(1 - remaining / total);
  }

  static double count(double current, double goal, {double minimum = 0}) {
    final range = goal - minimum;
    if (range <= 0) return current >= goal ? 1 : 0;
    return clamp((current - minimum) / range);
  }
}
