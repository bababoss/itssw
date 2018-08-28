
"""
Auther: Suresh
email: suresh@cogknit.com
"""
import cv2,time
class _video_reader(object):
    def __init__(self, video_file):
        self.video_file = video_file

    def __enter__(self):
        cap = cv2.VideoCapture(self.video_file)
        ret, frame = cap.read()  # can you read the source ?
        assert ret == True, "Video read error {}".format(self.video_file)
        #cap.set(1, 0)  # set it back to read first frame
        self.cap = cap
        return cap

    def __exit__(self, type, value, traceback):
        ''' TODO: Something intelligent if error occurs '''
        self.cap.release()
        return


class VideoObject(object):

    def __init__(self, video_file):
        self.file_path = video_file
        self.cap = cv2.VideoCapture(self.file_path)

    def get_frames(self, F=None):
        '''
        Get frames of a video one after the other as a list(generator)
        '''
        ret, frame = self.cap.read()
        while ret:
            yield F(frame) if F else frame
            ret, frame = cap.read()

    def pull_frames(self, frame_numbers=[], F=None):
        '''
        Get some specific frames of the video as a list(generator)
        '''
        for frame_number in frame_numbers:
            self.cap.set(1, frame_number)
            ret, frame = self.cap.read()
            if ret:
                yield F(frame) if F else frame


    @property
    def fps(self):

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.cap.release()
        return fps

    @property
    def width(self):
        fps = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.cap.release()
        return fps

    @property
    def height(self):
        fps = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.cap.release()
        return fps

    @property
    def length(self):
        f_count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.cap.release()
        return int(f_count)

    def __len__(self):
        return self.length









if __name__ == "__main__":
    path = "/home/cogknit/PycharmProjects/rnpd/media/scenemedia/output.mkv"
    vid = VideoObject(path)
    lists = vid.get_frames()
    print(type(lists), lists, end=' ')
    count = 0
    for i in lists:
        # print(i,end=' ')
        #cv2.imwrite("frames/{}%d.jpg".format("output") % count, i)
        #         cv2.imshow('image',i)
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()
        count += 1
        print(count, end=' ')

