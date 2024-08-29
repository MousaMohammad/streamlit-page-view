import ast
import subprocess
import tempfile
import os

class CodeTester:
    def __init__(self, ui_message_callback=None):
        self.ui_message_callback = ui_message_callback

    def send_message(self, message):
        """
        Send a message to the user interface.
        """
        if self.ui_message_callback:
            self.ui_message_callback(message)
        else:
            print(message)

    def clean_code(self, code: str):
        # Placeholder for any cleaning logic
        return code.strip()

    def check_syntax(self, code: str):
        try:
            ast.parse(code)
            self.send_message(":white_check_mark: Syntax is correct.")
            return True
        except SyntaxError as e:
            self.send_message(f":x: Syntax error: {e}")
            return False

    def check_executability(self, code):
        mock_input = lambda prompt='': 'mocked_input'
        exec_env = {'input': mock_input}
        
        try:
            exec(code, exec_env)
            self.send_message(":white_check_mark: Code executed successfully.")
            return True
        except Exception as e:
            self.send_message(f":x: Execution error: {e}")
            return False

    def run_tests(self, test_script: str, code_to_test: str):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                code_file_path = os.path.join(temp_dir, "code_to_test.py")
                test_file_path = os.path.join(temp_dir, "test_script.py")

                with open(code_file_path, 'w') as code_file:
                    code_file.write(code_to_test)

                with open(test_file_path, 'w') as test_file:
                    test_file.write(test_script)

                result = subprocess.run(['python3', '-m', 'unittest', 'discover', '-s', temp_dir, '-p', 'test_script.py'], capture_output=True, text=True)

                if result.returncode == 0:
                    self.send_message(f"All tests passed:\n{result.stdout}")
                    return True
                else:
                    self.send_message(f"Some tests failed: \n {result.stdout} \n {result.stderr}")
                    return False
        except Exception as e:
            self.send_message(f"Test execution failed: {e}")
            return False

    def check_single_code(self, code: str):
        self.send_message("Cleaning code...")
        code = self.clean_code(code)
        
        self.send_message("Checking syntax...")
        if not self.check_syntax(code):
            return False
        
        self.send_message("Checking executability...")
        if not self.check_executability(code):
            return False
        
        return True

    def check_code_with_tests(self, test_script: str, code_to_test: str):
        self.send_message("Cleaning test script and code script...")
        test_script = self.clean_code(test_script)
        code_to_test = self.clean_code(code_to_test)
        
        self.send_message("Checking syntax of the code script...")
        if not self.check_syntax(code_to_test):
            return False
        
        self.send_message("Checking executability of the code script...")
        if not self.check_executability(code_to_test):
            return False
        
        self.send_message("Checking syntax of the test script...")
        if not self.check_syntax(test_script):
            return False
        
        self.send_message("Checking executability of the test script...")
        if not self.check_executability(test_script):
            return False
        
        self.send_message("Running test script...")
        if not self.run_tests(test_script, code_to_test):
            return False
        
        return True

# Example usage:
code = """
class Chatbot: 
    def __init__(self): 
        pass

    def greet_user(self):
        return "Welcome to the Simple Chatbot!"

    def process_input(self, user_input):
        if not user_input:
            return "I'm sorry, I didn't catch that. Could you please repeat?"
        elif user_input.lower() == "hello":
            return "Hi there! How can I help you today?"
        else:
            return "I'm not sure how to respond to that. Can you try asking something else?"

if __name__ == "__main__":
    chatbot = Chatbot()
    print(chatbot.greet_user())
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        response = chatbot.process_input(user_input)
    print(f"Chatbot: {response}")
"""
test_cases = """
import unittest

class TestChatbot(unittest.TestCase):
    def setUp(self):
        self.chatbot = Chatbot()

def test_greet_user(self):
    greeting = self.chatbot.greet_user()
    self.assertEqual(greeting, "Welcome to the Simple Chatbot!")

def test_process_input_hello(self):
    response = self.chatbot.process_input("Hello")
    self.assertEqual(response, "Hi there! How can I help you today?")

def test_process_input_empty(self):
    response = self.chatbot.process_input("")
    self.assertEqual(response, "I'm sorry, I didn't catch that. Could you please repeat?")

def test_process_input_unknown(self):
    response = self.chatbot.process_input("XYZ123")
    self.assertEqual(response, "I'm not sure how to respond to that. Can you try asking something else?")

if __name__ == '__main__':
    unittest.main()
"""

tester = CodeTester()
result = tester.check_code_with_tests(test_cases, code)
print(result)