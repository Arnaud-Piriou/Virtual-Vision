import open3d
import argparse
import RealSenseRecorder
import atexit
import os
from Logger import Logger


def main() :

    os.system("cls")

    rootDir = os.path.join(os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop"), "Workspace")

    parser = argparse.ArgumentParser(description="Virtual Vision v0.0")

    parser.add_argument("--scan", action="store", nargs=1, default=1, type=int, required=True, help="Record a new scan of the environment : 0/1")
    parser.add_argument("--nsec", action="store", nargs=1, default=0, type=int, required=False, help="Set the scan duration in seconds (0 for unlimited, press Q to quit)")
    parser.add_argument("--workspace", action="store", nargs=1, default=rootDir, type=str, required=False, help="Workspace directory, Desktop/Workspace by default")
    parser.add_argument("--sharpening", action="store", nargs=1, default=0, type=int, required=False, help="Sharpen blurry images : 0/1")

    parser.add_argument("--fps", action="store", nargs=1, default=30, type=int, required=False, help="Set the RealSense framerate, default : 30")
    parser.add_argument("--width", action="store", nargs=1, default=1280, type=int, required=False, help="Set the RealSense width, default : 1280")
    parser.add_argument("--height", action="store", nargs=1, default=720, type=int, required=False, help="Set the RealSense height, default : 720")
    parser.add_argument("--vpreset", action="store", nargs=1, default=3, type=int, required=False, help="Set the RealSense visual preset (0 -> Custom, 1 -> Default, 2 -> Hand, 3 -> High Accuracy, 4 -> High Density, 5 -> Medium Density), default : 3")
    parser.add_argument("--laserpower", action="store", nargs=1, default=240, type=int, required=False, help="Set the RealSense laser power, default : 240")
    parser.add_argument("--exposure", action="store", nargs=1, default=3200, type=int, required=False, help="Set the RealSense exposure, default : 3200")
    parser.add_argument("--gain", action="store", nargs=1, default=16, type=int, required=False, help="Set the RealSense gain, default : 16")

    args = parser.parse_args()

    parameters = {
        "Scanning Mode" : bool(args.scan),
        "Scan Duration (s)" : args.nsec[0],
        "Workspace Root" : '"' + args.workspace + '"',
        "Sharpening RGB Frames" : bool(args.sharpening)
        }

    Logger.printParameters("PARAMETERS", parameters)

    if parameters["Scanning Mode"] :

        cameraParameters = {
            "FPS" : args.fps,
            "Width" : args.width,
            "Height" : args.height,
            "Visual Preset" :  args.vpreset,
            "Laser Power" :  args.laserpower,
            "Exposure" :  args.exposure,
            "Gain" :  args.gain
            }
        Logger.printParameters("CAMERA PARAMETERS", cameraParameters)
    
        Logger.printOperationTitle("SCANNING")

        rsr = RealSenseRecorder.RealSenseRecorder(
            scanDuration=parameters["Scan Duration (s)"], 
            fps=cameraParameters["FPS"], 
            width=cameraParameters["Width"], 
            height=cameraParameters["Height"], 
            visualPreset=cameraParameters["Visual Preset"], 
            laserPower=cameraParameters["Laser Power"], 
            exposure=cameraParameters["Exposure"], 
            gain=cameraParameters["Gain"], 
            rootDir=parameters["Workspace Root"].replace('"', ""), 
            sharpening=parameters["Sharpening RGB Frames"]
            )

        rsr.setupFolder()
        rsr.scan()
        
        atexit.register(rsr.close)


if __name__ == "__main__" :
    main()
