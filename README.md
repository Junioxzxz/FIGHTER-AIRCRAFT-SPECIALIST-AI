# Fighter Aircraft Specialist AI

A specialized AI assistant that provides comprehensive information about fighter aircraft, from early propeller-driven fighters to cutting-edge 6th generation aircraft.

## Features

- **Comprehensive Aircraft Knowledge**: Access detailed information about fighter aircraft spanning all generations
- **Technical Specifications**: Get precise data on performance, armament, and capabilities
- **Historical Context**: Learn about development histories and combat records
- **Comparative Analysis**: Compare different fighter models across eras and nations
- **Image Analysis**: Upload images of fighter aircraft for identification and detailed information

## Technologies Used

- Python 3.x
- Flask
- Google Generative AI (Gemini 1.5 Flash)
- TailwindCSS
- HTML/CSS/JavaScript

## Installation

1. Clone the repository:
```
git clone https://github.com/Junioxzxz/FIGHTER-AIRCRAFT-SPECIALIST-AI.git
cd fFIGHTER-AIRCRAFT-SPECIALIST-AI
```

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install required packages:
```
pip install -r requirements.txt
```

5. Set up your Gemini API key in the .env file:
```
GEMINI_API_KEY = "your_api_key_here"
```

## Usage

1. Start the Flask application:
```
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

3. Interact with the Fighter Aircraft Specialist AI by:
   - Asking questions about specific fighter jets
   - Requesting comparative analyses between different models
   - Uploading images of fighter aircraft for identification and information

## Example Queries

- "What are the specifications of the F-22 Raptor?"
- "Compare the dogfighting capabilities of the F-16 and MiG-29."
- "Describe the evolution of Soviet fighter jets during the Cold War."
- "What stealth features does the J-20 incorporate?"
- "Explain the weapons systems on the Eurofighter Typhoon."

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Google Generative AI for providing the Gemini API
- The aviation community for their valuable resources on fighter aircraft 
