import SwiftUI

public struct FrameSequenceView: View {
    public let progress: Double
    public let frameCount: Int
    public let imageName: (Int) -> String
    public let reducedMotion: Bool

    public init(
        progress: Double,
        frameCount: Int,
        reducedMotion: Bool = false,
        imageName: @escaping (Int) -> String
    ) {
        self.progress = progress
        self.frameCount = max(1, frameCount)
        self.reducedMotion = reducedMotion
        self.imageName = imageName
    }

    private var index: Int {
        let p = min(1, max(0, progress.isFinite ? progress : 0))
        if reducedMotion {
            if p < 0.25 { return 0 }
            if p < 0.75 { return max(0, (frameCount - 1) / 2) }
            return frameCount - 1
        }
        return min(frameCount - 1, Int((p * Double(frameCount - 1)).rounded()))
    }

    public var body: some View {
        Image(imageName(index))
            .resizable()
            .scaledToFit()
            .accessibilityHidden(true)
    }
}
