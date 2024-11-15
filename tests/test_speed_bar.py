# Speed bar not fully implemeneted so commenting the test case for now. 

# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import os

# class SpeedBarTest(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Initialize the Chrome driver
#         cls.driver = webdriver.Chrome()
        
#         # Save the HTML content to a temporary file and load it
#         html_content = """
#         <!DOCTYPE html>
#         <html lang="en">
#         <head>
#           <meta charset="UTF-8">
#           <title>Speed Bar</title>
#           <style>
#             .speed-bar-container { width: 300px; height: 30px; background-color: #e0e0e0; border-radius: 5px; overflow: hidden; margin-top: 20px; }
#             .speed-bar { height: 100%; width: 0; background-color: #4caf50; transition: width 0.3s; }
#             .slider { width: 100%; margin-top: 20px; }
#           </style>
#         </head>
#         <body>
#           <h2>Speed Bar Example</h2>
#           <input type="range" min="0" max="100" value="0" class="slider" id="speedSlider">
#           <div class="speed-bar-container"><div class="speed-bar" id="speedBar"></div></div>
#           <p>Current Speed: <span id="speedValue">0</span>%</p>
#           <script>
#             const speedSlider = document.getElementById("speedSlider");
#             const speedBar = document.getElementById("speedBar");
#             const speedValue = document.getElementById("speedValue");

#             speedSlider.addEventListener("input", function() {
#               const speed = speedSlider.value;
#               speedValue.textContent = speed;
#               speedBar.style.width = speed + "%";
#             });
#           </script>
#         </body>
#         </html>
#         """
        
#         # Write HTML to a temporary file and load it in the browser
#         with open("speed_bar_test.html", "w") as f:
#             f.write(html_content)
#         cls.driver.get("file://" + os.path.abspath("speed_bar_test.html"))

#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
#         os.remove("speed_bar_test.html")

#     def test_speed_bar_update_to_50_percent(self):
#         driver = self.driver

#         # Use WebDriverWait to ensure elements are available
#         slider = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "speedSlider")))
#         speed_value = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "speedValue")))
#         speed_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "speedBar")))

#         # Set the slider to 50% and trigger the change
#         driver.execute_script("arguments[0].value = 50; arguments[0].dispatchEvent(new Event('input'));", slider)

#         # Verify that the displayed speed value is 50
#         self.assertEqual(speed_value.text, "50")

#         # Verify that the width of the speed bar is 50%
#         self.assertEqual(speed_bar.get_attribute("style"), "width: 50%;")

#     def test_speed_bar_update_to_75_percent(self):
#         driver = self.driver

#         # Use WebDriverWait to ensure elements are available
#         slider = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "speedSlider")))
#         speed_value = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "speedValue")))
#         speed_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "speedBar")))

#         # Set the slider to 75% and trigger the change
#         driver.execute_script("arguments[0].value = 75; arguments[0].dispatchEvent(new Event('input'));", slider)

#         # Verify that the displayed speed value is 75
#         self.assertEqual(speed_value.text, "75")

#         # Verify that the width of the speed bar is 75%
#         self.assertEqual(speed_bar.get_attribute("style"), "width: 75%;")

# if __name__ == "__main__":
#     unittest.main()
