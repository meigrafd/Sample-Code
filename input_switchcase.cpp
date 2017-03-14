// http://www.forum-raspberrypi.de/Thread-c-c-swith-case-mit-char-array?pid=272160#pid272160

#include <iostream>
#include <string>

using namespace std;

int main() {
  string message;
  cout << "Enter something: ";
  getline(cin, message);

  for (int i=0; i < sizeof(message); ++i) {
    cout << message[i] << endl;
    switch (message[i]) {
      case 'h':
        cout << "burb!" << endl;
        break;
      case 'q':
        cout << "Quit!" << endl;
        break;
    }
  }
  return 0;
}