# BAXI 3523 AIRA — Lab Assessment 1 (From-Scratch Guide)

> **Note:** Replace `bXXXXXXXXX` with your actual **lowercase** matric number everywhere below.

---

## 1. Create the New ROS Package & Folders
*(If an old `nadiahhusna` folder already exists, delete it first with `rm -rf ~/catkin_ws/src/nadiahhusna`.)*

```bash
cd ~/catkin_ws/src
catkin_create_pkg nadiahhusna rospy geometry_msgs turtlesim
mkdir -p ~/catkin_ws/src/nadiahhusna/scripts
mkdir -p ~/catkin_ws/src/nadiahhusna/launch
```

---

## 2. Create & Make the Python Script Executable
Open a new Python file named with your lowercase matric number:

```bash
gedit ~/catkin_ws/src/nadiahhusna/scripts/bXXXXXXXXX.py
```

* Paste your `Catch_Bot` user-input code into the file.
* Add your personal details comment (**matric number, full name, section & group**) right after the library imports.
* Save and close `gedit`, then make the script executable:

```bash
chmod +x ~/catkin_ws/src/nadiahhusna/scripts/bXXXXXXXXX.py
```

---

## 3. Create the Launch File
Open a new launch file named with your lowercase name:

```bash
gedit ~/catkin_ws/src/nadiahhusna/launch/nadiahhusna.launch
```

Paste this exact XML and save:

```xml
<launch>
  <node pkg="turtlesim" type="turtlesim_node" name="sim" />
  <node pkg="nadiahhusna" type="bXXXXXXXXX.py" name="catch_and_catch" output="screen" launch-prefix="gnome-terminal --" />
</launch>
```

---

## 4. Build & Source Your Workspace

```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

---

## 5. Run the Simulation (Terminal 1)

```bash
roslaunch nadiahhusna nadiahhusna.launch
```

*(Wait for both the `turtlesim` window and the popup input terminal to appear.)*

---

## 6. Record the 30-Second ROS Bag (Terminal 2)
Open a **second terminal** and run:

```bash
cd ~/catkin_ws/src
rosbag record -a --duration=30 -O bXXXXXXXXX.bag
```

* Immediately switch to the popup input terminal and enter X and Y coordinates (between 2 and 10) so `turtle1` chases and catches `turtle2` during the 30 seconds.
* Recording will stop automatically after 30 seconds.
* Verify it saved properly:

```bash
rosbag info bXXXXXXXXX.bag
```

---

## 7. Zip Everything for Submission
Still inside `~/catkin_ws/src`, zip your package folder and `.bag` file into one single ZIP file:

```bash
cd ~/catkin_ws/src
zip -r nadiahhusna.zip nadiahhusna bXXXXXXXXX.bag
```

Your final `nadiahhusna.zip` will be inside `~/catkin_ws/src`, ready to submit.
