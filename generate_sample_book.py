from fpdf import FPDF
import os

def create_sample_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    title = "Physics: Electric Charges and Fields"
    text = """
    Chapter 1: Electric Charges and Fields
    
    1.1 Introduction
    Electromagnetism is a branch of physics involving the study of the electromagnetic force, a type of physical interaction that occurs between electrically charged particles. The electromagnetic force is carried by electromagnetic fields composed of electric fields and magnetic fields.
    
    1.2 Electric Charge
    Historically the credit of discovery of the fact that amber rubbed with wool or silk cloth attracts light objects goes to Thales of Miletus, Greece, around 600 BC. The name electricity is coined from the Greek word electron meaning amber.
    
    There are two kinds of electric charges: positive and negative. Like charges repel and unlike charges attract each other. The property which differentiates the two kinds of charges is called the polarity of charge.
    
    1.3 Conductors and Insulators
    Some substances readily allow passage of electricity through them, others do not. Those which allow electricity to pass through them easily are called conductors. Metals, human and animal bodies and earth are conductors. Most of the non-metals like glass, porcelain, plastic, nylon, wood offer high resistance to the passage of electricity through them. They are called insulators.
    
    1.4 Basic Properties of Electric Charge
    If the sizes of charged bodies are very small as compared to the distances between them, we treat them as point charges. All the charge content of the body is assumed to be concentrated at one point in space.
    
    Additivity of Charges: If a system contains two point charges q1 and q2, the total charge of the system is obtained simply by adding algebraically q1 and q2.
    
    Quantization of Charge: Experimentally it is established that all free charges are integral multiples of a basic unit of charge denoted by e. Thus charge q on a body is always given by q = ne, where n is any integer, positive or negative.
    
    Conservation of Charge: Within an isolated system, the total charge remains constant.
    """
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=title, ln=1, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)
    
    if not os.path.exists("books"):
        os.makedirs("books")
        
    pdf.output("books/Physics_Sample_Chapter.pdf")
    print("Sample PDF created successfully.")

if __name__ == "__main__":
    create_sample_pdf()
