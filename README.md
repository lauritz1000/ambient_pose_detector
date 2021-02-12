# Project for Ambient Interfaces: Bad Posture Detector

- Scenario:
	- Spending a lot of time in front of the computer and forget to take care of your posture, regularly

- Use case:
	Bobby is working an administration job at the university. He sits at the computer multiple hours per day and also most evenings he is gaming a few hours. He already notices that his back aches sometimes, and he heard of an easy application to keep track of his posture from a colleague. He decides to install it and try it out.
	He will continue with his work. At first he is aware of his posture, but after some time, he loses his focus and he sinks into his seat. The app detects that his posture is not correct. The tray application icon turns yellow or red, depending on the severeness. Bobby ignores it for now. After 5/15/30 minutes he will get a notification with a sound to remind him of his bad posture. He fixes his posture and the tray icon will turn green again.

- motivation
	- fix back/eye problems
	- take of his posture/health
	- don't want to sit to close to the screen

- context:
	- office or at home?
	- best case, only one person present in the picture
	- clothes, sunglasses, hair, hats, etc.: do they conflict with the detection?
	- how much of the body is seen

- Initiation:
    - install 1-time
    - autostart every time the computer is started
- Awareness of the system:
    - look at graph
    - notification/sound
    - (disrupt your image/etc. to fix it fix posture)
- configuration:
    - adjust scale according to the picture in the app

- design:
	- graph shows posture of the last 15 minutes
	- notification/sound if bad posture is detected
	- tray icon changes color based on posture

- implementation:
    - always ai for human posture detection
    - pystray for tray application
    - web app for configuration of the scale etc.

- potential problems:
    - needs a lot of horsepower:
        - only check every few seconds/minutes/etc.
        - run on a server
    - posture configurator:
        - every human is different
        - camera positioned differently
    - false detections:
        - obstacles/hands/etc. will trigger bad posture detections
    - tray icon not activated on all systems
