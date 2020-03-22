#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <map>

//using namespace std;
//using namespace cv;


std::map<std::string, std::tuple<cv::Scalar_<double>, cv::Scalar_<double>>> colours = {
  {"Rojo", std::make_tuple(cv::Scalar(155,25,0), cv::Scalar(179,255,255))},
  {"Azul", std::make_tuple(cv::Scalar(100,200,50), cv::Scalar(140,255,255))}
};

//colours = {"Rojo": (Scalar(155,25,0), Scalar(179,255,255)),
//           "Azul": (Scalar(100,200,200), Scalar(140,255,255))
//           }

cv::Mat colorFilter(const cv::Mat& src, std::tuple<cv::Scalar_<double>, cv::Scalar_<double>> hsvInterval)
{
  assert(src.type() == CV_8UC3);
  cv::Mat colour;
  inRange(src, std::get<0>(hsvInterval), std::get<1>(hsvInterval), colour);
  return colour;
}


int main( int argc, char** argv )
{
  cv::VideoCapture cap(0); //capture the video from web cam

  if ( !cap.isOpened() )  // if not success, exit program
  {
    std::cout << "Cannot open the web cam" << std::endl;
    return -1;
  }
   //inRange(imgHSV, Scalar(iLowH, iLowS, iLowV), Scalar(iHighH, iHighS, iHighV), imgThresholded); //Threshold the image

  while (true)
  {
    cv::Mat imgOriginal;

    bool bSuccess = cap.read(imgOriginal); // read a new frame from video

    if (!bSuccess) //if not success, break loop
    {
      std::cout << "Cannot read a frame from video stream" << std::endl;
      break;
    }

    cv::Mat imgHSV;

    cv::cvtColor(imgOriginal, imgHSV, cv::COLOR_BGR2HSV); //Convert the captured frame from BGR to HSV

    cv::Mat imgThresholded;

    std::map<std::string, std::tuple<cv::Scalar_<double>, cv::Scalar_<double>>>::iterator it = colours.begin();
    for (std::pair<std::string, std::tuple<cv::Scalar_<double>, cv::Scalar_<double>>> element : colours) {

      imgThresholded = colorFilter(imgHSV, element.second);

      int numWhitePixels = cv::countNonZero(imgThresholded);
      if (numWhitePixels > 10000) {
        std::cout << element.first << ": "<< numWhitePixels << '\n';

        cv::Mat result;
        cv::bitwise_and(imgOriginal, imgOriginal, result, imgThresholded);

        cv::imshow("Result Image", result); //show the thresholded image
        cv::imshow("Original", imgOriginal); //show the original image
      }
    }

    //morphological closing (fill small holes in the foreground)
    //cv::dilate(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(5, 5)));
    //cv::erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(5, 5)));

    if (cv::waitKey(30) == 27) //wait for 'esc' key press for 30ms. If 'esc' key is pressed, break loop
    {
      std::cout << "esc key is pressed by user" << std::endl;
      break;
    }
  }
  return 0;
}
