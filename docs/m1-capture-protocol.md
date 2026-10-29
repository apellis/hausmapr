# M1 photo capture protocol

For each test room, take one deliberately "good" photo set and one "messy" set, so M1 tells us both the best case and the realistic case.

## Setup

- Turn on all the lights and open the curtains. Avoid direct sun streaks if possible.
- Prop the printed calibration board (`markers/charuco_letter.pdf`) against a wall at roughly waist height, then move it to a second wall halfway through the capture. Two positions let us check scale twice.
- If your phone has LiDAR (iPhone Pro, iPad Pro), also do one capture with a LiDAR scanning app that exports its raw photos and depth, such as the ones in the spec. That's our LiDAR comparison.

## Good set (40-80 photos)

1. Stand in each corner and take 3 photos sweeping across the opposite walls, holding the phone level.
2. Walk the room's perimeter about 1 m from the walls, taking a photo every step and pointing at the wall opposite.
3. Take 4-6 photos of the ceiling and 4-6 of the floor, with some wall in each frame.
4. Take 2-3 photos of every door and window, including the frame edges.

Every photo should overlap its neighbour by about two thirds. Don't use zoom or portrait mode, and keep the camera on the main 1x lens.

## Messy set (whatever comes naturally)

Walk in and take photos the way you would if no one had told you how, 20-60 of them. This approximates real users.

## Where to put the files

`data/captures/<room id>/good/` and `data/captures/<room id>/messy/`. Keep the original files (HEIC or JPEG). The metadata matters, so don't send them through a messaging app first. Photos stay out of git; see `.gitignore`.
