import openai
import pytesseract
from pdf2image import convert_from_path
import requests
import pandas as pd
import streamlit as st

def extract_text_from_pdf(file_path):
    """Extract text from blueprint PDF using OCR."""
    try:
        images = convert_from_path(file_path)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
        return text
    except Exception as e:
        st.error(f"Failed to extract text from PDF: {e}")
        return ""

def analyze_plan_with_ai(plan_text):
    """Use OpenAI to analyze the construction plan and extract details."""
    prompt = (
        f"""Extract room sizes, materials needed, and labor categories from the following construction plan:
        {plan_text}
        """
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an expert in construction plan analysis."},
                      {"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.OpenAIError as e:
        st.error(f"OpenAI API error: {e}")
        return ""

def get_data_from_api(api_url, error_message):
    """Fetch data from an API and handle errors."""
    try:
        response = requests.get(api_url)  # Replace with actual API
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"{error_message}: {e}")
    return {}

def calculate_project_cost(materials_needed, labor_hours):
    """Calculate material and labor costs based on real-time prices."""
    material_prices = get_data_from_api("https://api.example.com/materials", "Error fetching material prices")
    labor_rates = get_data_from_api("https://api.example.com/labor", "Error fetching labor costs")
    
    material_costs = {mat: materials_needed.get(mat, 0) * material_prices.get(mat, 0) for mat in materials_needed}
    labor_costs = {job: labor_hours.get(job, 0) * labor_rates.get(job, 0) for job in labor_hours}
    
    return material_costs, labor_costs

def generate_cost_report(material_costs, labor_costs):
    """Generate a detailed cost estimation report."""
    df_materials = pd.DataFrame(material_costs.items(), columns=["Material", "Cost ($)"])
    df_labor = pd.DataFrame(labor_costs.items(), columns=["Labor Type", "Cost ($)"])
    
    total_cost = sum(material_costs.values()) + sum(labor_costs.values())
    return df_materials, df_labor, total_cost

def main():
    st.title("AI Construction Cost Estimator")
    uploaded_file = st.file_uploader("Upload Construction Plan (PDF)", type=["pdf"])
    
    if uploaded_file is not None:
        plan_text = extract_text_from_pdf(uploaded_file)
        if not plan_text:
            return
        
        analyzed_data = analyze_plan_with_ai(plan_text)
        if not analyzed_data:
            return
        
        st.subheader("Analyzed Plan Data")
        st.write(analyzed_data)
        
        # Example material and labor information
        materials_needed = {"concrete": 100, "steel": 5, "wood": 200}
        labor_hours = {"electrician": 50, "plumber": 40, "carpenter": 60}
        
        material_costs, labor_costs = calculate_project_cost(materials_needed, labor_hours)
        df_materials, df_labor, total_cost = generate_cost_report(material_costs, labor_costs)
        
        st.subheader("Material Cost Breakdown")
        st.dataframe(df_materials)
        
        st.subheader("Labor Cost Breakdown")
        st.dataframe(df_labor)
        
        st.subheader("Total Estimated Cost")
        st.write(f"${total_cost:.2f}")

if __name__ == "__main__":
    main()
