!pip install flask 
python 
   from flask import Flask, render_template, request, jsonify 
   from threading import Thread 
   app = Flask(_name_) 
 
   # Sample resume templates 
   TEMPLATES = { 
       "professional": "professional.html", 
       "modern": "modern.html", 
       "creative": "creative.html", 
   } 
 
   # Sample function to match skills (basic implementation) 
   def match_skills(resume_text, job_description): 
       resume_skills = set(resume_text.lower().split()) 
       job_skills = set(job_description.lower().split()) 
       matched_skills = resume_skills.intersection(job_skills) 
       return list(matched_skills) 
 
   @app.route("/") 
   def home(): 
       return render_template("index.html") 
 
   @app.route("/generate", methods=["POST"]) 
   def generate_resume(): 
       data = request.json 
       resume_text = data.get("resume_text", "") 
       job_description = data.get("job_description", "") 
       template = data.get("template", "professional") 
 
       # Match skills (basic implementation) 
       matched_skills = match_skills(resume_text, job_description) 
 
       # Render the selected template 
       template_file = TEMPLATES.get(template, TEMPLATES["professional"]) 
       with open(template_file, "r") as file: 
           resume_html = file.read() 
 
       # Replace placeholders with actual data 
       resume_html = resume_html.replace("{{ skills }}", ", ".join(matched_skills)) 
       resume_html = resume_html.replace("{{ resume_text }}", resume_text) 
 
       return jsonify({"resume_html": resume_html}) 
 
   def run_flask(): 
       app.run(host="0.0.0.0", port=5000) 
 
   # Start Flask in a background thread 
   flask_thread = Thread(target=run_flask) 
   flask_thread.start() 
    
 
 
   python 
   %%writefile index.html 
   <!DOCTYPE html> 
   <html lang="en"> 
   <head> 
       <meta charset="UTF-8"> 
       <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
       <title>SmartResume Generator</title> 
       <style> 
           body { font-family: Arial, sans-serif; margin: 20px; } 
           textarea { width: 100%; height: 150px; margin-bottom: 10px; } 
           .output { margin-top: 20px; border: 1px solid #ccc; padding: 20px; } 
       </style> 
   </head> 
   <body> 
       <h1>SmartResume Generator</h1> 
       <form id="resumeForm"> 
           <label for="resumeText">Paste Your Resume:</label><br> 
           <textarea id="resumeText" placeholder="Enter your resume text here..."></textarea><br> 
 
           <label for="jobDescription">Paste Job Description:</label><br> 
           <textarea id="jobDescription" placeholder="Enter the job description here..."></textarea><br> 
 
           <label for="template">Choose Template:</label> 
           <select id="template"> 
               <option value="professional">Professional</option> 
               <option value="modern">Modern</option> 
               <option value="creative">Creative</option> 
           </select><br><br> 
 
           <button type="button" onclick="generateResume()">Generate Resume</button> 
       </form> 
 
       <div class="output" id="output"> 
           <!-- Generated resume will appear here -->

</div> 
 
       <script> 
           async function generateResume() { 
               const resumeText = document.getElementById("resumeText").value; 
               const jobDescription = document.getElementById("jobDescription").value; 
               const template = document.getElementById("template").value; 
 
               const response = await fetch("/generate", { 
                   method: "POST", 
                   headers: { 
                       "Content-Type": "application/json", 
                   }, 
                   body: JSON.stringify({ 
                       resume_text: resumeText, 
                       job_description: jobDescription, 
                       template: template, 
                   }), 
               }); 
 
               const data = await response.json(); 
               document.getElementById("output").innerHTML = data.resume_html; 
           } 
       </script> 
   </body> 
   </html> 
    
 
   Repeat this for `professional.html`, `modern.html`, and `creative.html`. 
 
   python 
   !pip install pyngrok 
   from pyngrok import ngrok 
 
   # Start ngrok tunnel 
   public_url = ngrok.connect(5000) 
   print("Public URL:", public_url) 
    
 