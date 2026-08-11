%% Cricket Bowling Analytics
% ============================================================
% Week 2 - Video Processing Module
% ============================================================
%
% PURPOSE:
% This script is responsible for the FIRST stage of our system:
%
%       Select Video
%            ↓
%       Read Video
%            ↓
%       Get Video Information
%            ↓
%       Choose Start / End
%            ↓
%       Trim Video
%            ↓
%       Read Trimmed Video Frame-by-Frame
%            ↓
%       Display Trimmed Frames
%
% IMPORTANT:
% We are NOT doing pose estimation yet.
%
% This module only handles the input video and prepares the
% relevant bowling segment for the next stage.
%
% Later, the output of this module will be passed to:
%
%       Pose Estimation
%            ↓
%       Bowling Analysis
%
% ============================================================


%% 1. Clear MATLAB environment

clc;
% clc clears the Command Window.
% It removes old text so that our output is easier to read.

clear;
% clear removes variables from the MATLAB workspace.
% This prevents variables from an older program affecting
% our current program.

close all;
% close all closes any figures that may already be open.


%% 2. Select the bowling video

% uigetfile() opens a file-selection dialog box.
%
% Eventually our coach will select the video using the GUI.
% For now, we are using MATLAB's built-in file selector.
%
% The first output is:
%       fileName -> name of the selected video
%
% The second output is:
%       filePath -> folder containing the video

[fileName, filePath] = uigetfile( ...
    {'*.mp4;*.avi;*.mov', ...
     'Video Files (*.mp4, *.avi, *.mov)'}, ...
    'Select a Bowling Video');


%% 3. Check whether the user cancelled the selection

% If the user presses Cancel,
% uigetfile() returns 0.

if isequal(fileName, 0)

    disp("No video selected.");

    % return stops the script here.
    % We don't want the rest of the code to run
    % without a video.

    return;

end


%% 4. Create the complete video path

% filePath contains something like:
%
%       /MATLAB Drive/CricketBowlingAnalytics/data/raw/sample_videos/
%
% fileName contains something like:
%
%       balling vdo sample 1.mp4
%
% fullfile() safely combines them into:
%
%       /MATLAB Drive/CricketBowlingAnalytics/data/raw/
%       sample_videos/balling vdo sample 1.mp4

videoPath = fullfile(filePath, fileName);


% Display the selected file in the Command Window.

fprintf("\nSelected video: %s\n", fileName);


%% 5. Create a VideoReader object

% VideoReader allows MATLAB to work with a video.
%
% IMPORTANT:
%
% This does NOT mean that MATLAB loads the entire video
% into memory.
%
% Instead, VideoReader gives us an object through which
% we can access the video frame-by-frame.

video = VideoReader(videoPath);


%% 6. Read and display video information

fprintf("\n========== VIDEO INFORMATION ==========\n");


% Name of the video file

fprintf("File name      : %s\n", fileName);


% Duration tells us how long the video is in seconds.

fprintf("Duration       : %.2f seconds\n", ...
    video.Duration);


% FrameRate tells us how many frames exist per second.
%
% Example:
%
%       60 FPS
%
% means approximately 60 frames are present
% in every second of video.

fprintf("Frame rate     : %.2f FPS\n", ...
    video.FrameRate);


% Width of each frame in pixels.

fprintf("Width          : %d pixels\n", ...
    video.Width);


% Height of each frame in pixels.

fprintf("Height         : %d pixels\n", ...
    video.Height);


%% 7. Estimate total number of frames

% Approximately:
%
%       Number of Frames
%             =
%       Duration × Frame Rate
%
% Example:
%
%       10 seconds × 60 FPS
%       = approximately 600 frames
%
% We use floor() to get an integer.
%
% NOTE:
% This is only an estimate. Later, when exact frame
% indexing becomes important, we will handle it separately.

totalFrames = floor( ...
    video.Duration * video.FrameRate);


fprintf("Approx frames  : %d\n", totalFrames);

fprintf("========================================\n");


%% 8. Choose the relevant bowling segment

% Our sample video contains some unwanted footage before
% the actual bowling action.
%
% For example:
%
%       0 sec ---------------------------- 7.92 sec
%       |                                  |
%       Waiting       Bowling              End
%                         ↑
%                  Relevant segment
%
% We don't want to send all of this unnecessary footage
% to the future pose-estimation module.
%
% For now, we manually enter the start and end times.
%
% Later, Week 3's GUI will provide a much better way
% to select these values.


% Ask the user for the starting time.

startTime = input( ...
    "\nEnter START time in seconds: ");


% Ask the user for the ending time.

endTime = input( ...
    "Enter END time in seconds: ");


%% 9. Validate the selected time range

% Start time cannot be negative.

if startTime < 0

    error("Start time cannot be negative.");

end


% Start time must be inside the video.

if startTime >= video.Duration

    error("Start time must be within the video duration.");

end


% End time must be greater than start time.

if endTime <= startTime

    error("End time must be greater than start time.");

end


% End time cannot be beyond the original video duration.

if endTime > video.Duration

    error("End time exceeds the video duration.");

end


%% 10. Find the project root folder

% Our current script is located at:
%
% CricketBowlingAnalytics/
%       src/
%           video_processing/
%               videoProcessingDemo.m
%
% We need to go back to the project root so that we can
% save the trimmed video inside:
%
%       data/processed/
%
%
% mfilename('fullpath') gives the complete path of the
% currently running script.

thisFile = mfilename('fullpath');


% fileparts() extracts the folder containing the script.

videoProcessingFolder = fileparts(thisFile);


% Move one level upward:
%
% video_processing → src

srcFolder = fileparts(videoProcessingFolder);


% Move one more level upward:
%
% src → CricketBowlingAnalytics

projectRoot = fileparts(srcFolder);


%% 11. Create the processed-video folder path

% We want our trimmed video to be saved here:
%
% CricketBowlingAnalytics/
%       data/
%           processed/

processedFolder = fullfile( ...
    projectRoot, ...
    "data", ...
    "processed");


%% 12. Create the processed folder if necessary

% isfolder() checks whether the folder already exists.

if ~isfolder(processedFolder)

    % mkdir() creates the folder if it does not exist.

    mkdir(processedFolder);

end


%% 13. Create a name for the trimmed video

% We do NOT want to overwrite the original video.
%
% Example:
%
% Original:
%       balling vdo sample 1.mp4
%
% Trimmed:
%       balling vdo sample 1_trimmed.mp4


% fileparts() separates the filename from its extension.
%
% We only need the original filename here.

[~, originalName, ~] = fileparts(fileName);


% Create the new filename.

trimmedFileName = sprintf( ...
    "%s_trimmed.avi", ...
    originalName);


% Create the complete path where the trimmed video
% will be saved.

trimmedVideoPath = fullfile( ...
    processedFolder, ...
    trimmedFileName);


%% 14. CALL THE trimVideo FUNCTION

% THIS IS THE IMPORTANT PART.
%
% trimVideo() is a separate MATLAB function located in:
%
%       src/video_processing/trimVideo.m
%
% We are passing four things to it:
%
% 1. videoPath
%       → original video
%
% 2. startTime
%       → where the relevant segment starts
%
% 3. endTime
%       → where the relevant segment ends
%
% 4. trimmedVideoPath
%       → where the new video should be saved
%
% The actual trimming logic is inside trimVideo.m.
%
% Our current script simply CALLS that function.

trimVideo( ...
    videoPath, ...
    startTime, ...
    endTime, ...
    trimmedVideoPath);


%% 15. Open the newly trimmed video

% We DON'T want to process the original video anymore.
%
% From this point onward, we work only with the
% trimmed bowling segment.

trimmedVideo = VideoReader(trimmedVideoPath);


%% 16. Display information about the trimmed video

fprintf("\n========== TRIMMED VIDEO ==========\n");

fprintf("Trimmed file   : %s\n", ...
    trimmedFileName);

fprintf("Start time     : %.2f seconds\n", ...
    startTime);

fprintf("End time       : %.2f seconds\n", ...
    endTime);

fprintf("Duration       : %.2f seconds\n", ...
    trimmedVideo.Duration);

fprintf("Frame rate     : %.2f FPS\n", ...
    trimmedVideo.FrameRate);

fprintf("===================================\n");


%% 17. Prepare for trimmed-frame processing

% frameNumber keeps track of how many frames we have
% processed from the trimmed video.

frameNumber = 0;


% Create a figure window where the trimmed video
% will be displayed.

figure('Name', 'Trimmed Bowling Video');


%% 18. Read the TRIMMED video one frame at a time

% hasFrame(trimmedVideo) checks whether another frame
% is available in the trimmed video.

while hasFrame(trimmedVideo)


    %% 18.1 Read the next frame

    % readFrame() reads ONE frame.

    frame = readFrame(trimmedVideo);


    %% 18.2 Increase frame counter

    frameNumber = frameNumber + 1;


    %% 18.3 Display the current frame

    imshow(frame);


    %% 18.4 Display frame information

    % We display:
    %
    %       Current frame number
    %       Current time within the trimmed video

    title(sprintf( ...
        "Trimmed Frame: %d | Time: %.2f seconds", ...
        frameNumber, ...
        trimmedVideo.CurrentTime));


    %% 18.5 Update the figure immediately

    % drawnow forces MATLAB to update the figure.

    drawnow;

end


%% 19. Display completion message

fprintf("\n========================================\n");

fprintf("Video processing completed successfully.\n");

fprintf("Trimmed frames processed: %d\n", ...
    frameNumber);

fprintf("Trimmed video saved at:\n%s\n", ...
    trimmedVideoPath);

fprintf("========================================\n");