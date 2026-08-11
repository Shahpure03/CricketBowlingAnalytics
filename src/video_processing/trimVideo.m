function outputPath = trimVideo(videoPath, startTime, endTime, outputPath)
% ============================================================
% trimVideo
% ============================================================
%
% PURPOSE:
% This function extracts only the required portion of a video.
%
% INPUTS:
%
% videoPath  -> Full path of the original video
%
% startTime  -> Time (in seconds) where the required video starts
%
% endTime    -> Time (in seconds) where the required video ends
%
% outputPath -> Where the trimmed video should be saved
%
% OUTPUT:
%
% outputPath -> Path of the newly created trimmed video
%
% ============================================================


%% 1. Open the original video

% VideoReader allows us to read the original video
% frame-by-frame.

video = VideoReader(videoPath);


%% 2. Validate the start and end times

% Start time cannot be negative.

if startTime < 0
    error("Start time cannot be negative.");
end


% End time must be greater than start time.

if endTime <= startTime
    error("End time must be greater than start time.");
end


% End time cannot be beyond the actual video duration.

if endTime > video.Duration
    error("End time exceeds the video duration.");
end


%% 3. Create a VideoWriter object

% VideoWriter allows us to create a new video file.

outputVideo = VideoWriter(outputPath, "Motion JPEG AVI");


% Keep the same frame rate as the original video.

outputVideo.FrameRate = video.FrameRate;


% Open the output video for writing.

open(outputVideo);


%% 4. Move to the beginning of the required section

% CurrentTime tells VideoReader where we currently are
% in the video.

video.CurrentTime = startTime;


%% 5. Read only the required section

while hasFrame(video)

    % Stop when we reach the requested end time.

    if video.CurrentTime > endTime
        break;
    end


    % Read the current frame.

    frame = readFrame(video);


    % Write the frame into the new video.

    writeVideo(outputVideo, frame);

end


%% 6. Close the output video

% Always close VideoWriter after writing.

close(outputVideo);


%% 7. Tell the user where the file was created

fprintf("\nTrimmed video created successfully.\n");
fprintf("Saved at: %s\n", outputPath);

end