// define env vars NPTRACKINGTOOLS_INC NPTRACKINGTOOLS_LIB in VS project properties C:\Program Files\OptiTrack\Motive\inc
#include "NPTrackingTools.h"

// we need UserProfile.xml and camera calibration Calibration.cal

int main()
{
// Initializing all connected cameras
    TT_Initialize();
    TT_LoadProfile("UserProfile.xml"); 	// Loading application profile, UserProfile.xml
    TT_LoadCalibration("CameraCal.cal"); 	// Loading CAL file hmmm strona po japonsku/chinsku/koreansku nie odczytalem kalibracji

    int cameraCount = TT_CameraCount();
    int intensity = 10;
    int framerate = 100;
    // set cameras settings 
    for (int i = 0; i < cameraCount; i++)
    {
        TT_SetCameraSettings(i, TT_CameraVideoType(i), TT_CameraExposure(i), TT_CameraThreshold(i), intensity);
        TT_SetCameraFrameRate(i, framerate);

        //== Outputting the Settings ==//
        printf("Camera #%d:\n", i);
        printf("\tFPS: %d\n\tIntensity: %d\n\tExposure: %d\n\tIntensity: %d\n\tVideo Type:%d\n", TT_CameraFrameRate(i), TT_CameraIntensity(i),
                TT_CameraExposure(i), TT_CameraIntensity(i),TT_CameraVideoType(i));
    }

    int frameCounter = 0; // Frame counter variable
 	while (!_kbhit())
	{
		if(TT_Update() == NPRESULT_SUCCESS)
		{
			// Each time the TT_Update function successfully updates the frame,
			// the frame counter is incremented, and the new frame is processed.
			frameCounter++;

			////// PROCESS NEW FRAME //////
            int totalMarker = TT_FrameMarkerCount();
            printf("Frame #%d: (Markers: %d)\n", framecounter, totalMarker);

            for (int i = 0 ; i < totalMarker; i++)
            {
                printf("\tMarker #%d:\t(%.2f,\t%.2f,\t%.2f)\n\n", i, TT_FrameMarkerX(i), TT_FrameMarkerY(i), TT_FrameMarkerZ(i));
            }
		}
	}
    // Closing down all of the connected cameras

    TT_Shutdown();
    return 0;
}