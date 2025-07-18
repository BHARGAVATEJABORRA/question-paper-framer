import os
import requests
from tqdm import tqdm
from fpdf import FPDF
from git import Repo

subjectsDatabase = {
    "CSE": {
        "1": ["Mathematics-I", "Engineering Physics", "Programming Fundamentals", "Engineering Graphics", "Environmental Science"],
        "2": ["Data Structures & Algorithms", "Digital Logic Design", "Discrete Mathematics", "Object Oriented Programming", "Database Management Systems"],
        "3": ["Operating Systems", "Computer Networks", "Software Engineering", "Theory of Computation", "Web Technologies", "Machine Learning"],
        "4": ["Artificial Intelligence", "Cloud Computing", "Big Data Analytics", "Cybersecurity", "Internet of Things", "Project Work"]
    },
    "ECE": {
        "1": ["Mathematics-I", "Engineering Chemistry", "Basic Electronics", "Engineering Graphics", "English Communication"],
        "2": ["Signals and Systems", "Analog Circuits", "Digital Electronics", "Probability Theory", "Network Analysis"],
        "3": ["Microprocessors", "Communication Systems", "Control Systems", "VLSI Design", "Embedded Systems"],
        "4": ["Wireless Communication", "Optical Communication", "Microwave Engineering", "Antenna Theory", "Project Work"]
    },
    "MECH": {
        "1": ["Mathematics-I", "Engineering Physics", "Engineering Mechanics", "Engineering Graphics", "Workshop Practice"],
        "2": ["Thermodynamics", "Fluid Mechanics", "Strength of Materials", "Manufacturing Processes", "Machine Drawing"],
        "3": ["Heat Transfer", "Dynamics of Machines", "Machine Design", "Industrial Engineering", "CAD/CAM"],
        "4": ["Automobile Engineering", "Robotics", "Finite Element Analysis", "Refrigeration & Air Conditioning", "Project Work"]
    },
    "EEE": {
        "1": ["Mathematics-I", "Engineering Chemistry", "Basic Electrical Engineering", "Engineering Graphics", "English Communication"],
        "2": ["Circuit Theory", "Electromagnetic Fields", "Analog Electronics", "Digital Electronics", "Signals and Systems"],
        "3": ["Power Systems", "Control Systems", "Electrical Machines", "Power Electronics", "Microprocessors"],
        "4": ["High Voltage Engineering", "Renewable Energy Systems", "Electrical Drives", "Smart Grid", "Project Work"]
    },
    "CIVIL": {
        "1": ["Mathematics-I", "Engineering Physics", "Engineering Mechanics", "Engineering Graphics", "Environmental Science"],
        "2": ["Strength of Materials", "Fluid Mechanics", "Surveying", "Building Materials", "Engineering Geology"],
        "3": ["Structural Analysis", "Geotechnical Engineering", "Transportation Engineering", "Water Resources Engineering", "Concrete Technology"],
        "4": ["Environmental Engineering", "Design of Structures", "Construction Management", "Remote Sensing", "Project Work"]
    }
}

# Example of known PDF sources for some subjects (optional)
sample_sources = {
    # 'Operating Systems': 'https://example.com/os_sample.pdf'
}

def fetch_pdf(url):
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and 'application/pdf' in r.headers.get('Content-Type', ''):
            return r.content
    except Exception:
        pass
    return None

class DummyPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, self.title, ln=True, align='C')
        self.ln(10)

def generate_dummy_pdf(path, subject, branch, year, paper_type):
    pdf = DummyPDF()
    pdf.title = f"{subject} - {paper_type}"
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(0, 10, f"Branch: {branch}\nYear: {year}\nThis is a placeholder question paper for {subject} ({paper_type}).")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pdf.output(path)


def ensure_lfs_tracking():
    attribute_line = 'sample_papers/** filter=lfs diff=lfs merge=lfs -text\n'
    if os.path.exists('.gitattributes'):
        with open('.gitattributes', 'r+') as f:
            content = f.read()
            if 'sample_papers/**' not in content:
                if not content.endswith('\n'):
                    f.write('\n')
                f.write(attribute_line)
    else:
        with open('.gitattributes', 'w') as f:
            f.write(attribute_line)


def main():
    ensure_lfs_tracking()
    repo = Repo('.')
    paper_types = {
        'mid': 'Mid Semester',
        'final': 'Final Exam',
        'quiz': 'Quiz',
        'mock': 'Mock Test'
    }
    tasks = []
    for branch, years in subjectsDatabase.items():
        for year, subjects in years.items():
            for pkey in paper_types.keys():
                for subject in subjects:
                    filename = subject.replace(' ', '_') + '.pdf'
                    path = os.path.join('sample_papers', branch, year, pkey, filename)
                    tasks.append((subject, branch, year, pkey, paper_types[pkey], path))

    for subject, branch, year, key, label, path in tqdm(tasks, desc='Processing'):
        if os.path.exists(path):
            continue
        content = None
        if subject in sample_sources:
            content = fetch_pdf(sample_sources[subject])
        if content:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                f.write(content)
        else:
            generate_dummy_pdf(path, subject, branch, year, label)

    repo.git.add('sample_papers')
    repo.git.add('.gitattributes')
    if repo.is_dirty():
        repo.index.commit('Add generated sample question papers')

if __name__ == '__main__':
    main()
