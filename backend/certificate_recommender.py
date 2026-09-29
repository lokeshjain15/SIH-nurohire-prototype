# =========================================================
# NEUROHIRE - SMART CERTIFICATION RECOMMENDATION ENGINE
# Final SIH-ready version with clickable learning resources
# =========================================================

from urllib.parse import quote_plus


CERTIFICATE_MAP = {'python': [{'name': 'Python for Everybody',
             'provider': 'Coursera',
             'level': 'Beginner',
             'category': 'Programming',
             'url': 'https://www.coursera.org/specializations/python',
             'estimated_effort': '8-20 hours',
             'resource_type': 'Certification / Learning Path'}],
 'java': [{'name': 'Java Programming and Software Engineering Fundamentals',
           'provider': 'Coursera',
           'level': 'Beginner',
           'category': 'Programming',
           'url': 'https://www.google.com/search?q=Java+Programming+and+Software+Engineering+Fundamentals+Coursera',
           'estimated_effort': '8-20 hours',
           'resource_type': 'Certification / Learning Path'}],
 'javascript': [{'name': 'Meta Front-End Developer Professional Certificate',
                 'provider': 'Meta',
                 'level': 'Beginner',
                 'category': 'Web Development',
                 'url': 'https://www.coursera.org/professional-certificates/meta-front-end-developer',
                 'estimated_effort': '8-20 hours',
                 'resource_type': 'Certification / Learning Path'}],
 'c++': [{'name': 'C++ Programming Learning Path',
          'provider': 'Coursera',
          'level': 'Intermediate',
          'category': 'Programming',
          'url': 'https://www.google.com/search?q=C%2B%2B+Programming+Learning+Path+Coursera',
          'estimated_effort': '15-40 hours',
          'resource_type': 'Certification / Learning Path'}],
 'sql': [{'name': 'SQL for Data Science',
          'provider': 'Coursera',
          'level': 'Beginner',
          'category': 'Data',
          'url': 'https://www.coursera.org/learn/sql-for-data-science',
          'estimated_effort': '8-20 hours',
          'resource_type': 'Certification / Learning Path'}],
 'excel': [{'name': 'Microsoft Excel Professional Certificate',
            'provider': 'Microsoft',
            'level': 'Beginner',
            'category': 'Data Analytics',
            'url': 'https://www.google.com/search?q=Microsoft+Excel+Professional+Certificate+Microsoft',
            'estimated_effort': '8-20 hours',
            'resource_type': 'Certification / Learning Path'}],
 'power bi': [{'name': 'Microsoft Power BI Data Analyst',
               'provider': 'Microsoft',
               'level': 'Intermediate',
               'category': 'Data Visualization',
               'url': 'https://learn.microsoft.com/en-us/credentials/certifications/data-analyst-associate/',
               'estimated_effort': '15-40 hours',
               'resource_type': 'Certification / Learning Path'}],
 'tableau': [{'name': 'Tableau Business Intelligence Analyst',
              'provider': 'Tableau',
              'level': 'Intermediate',
              'category': 'Data Visualization',
              'url': 'https://www.tableau.com/learn/certification',
              'estimated_effort': '15-40 hours',
              'resource_type': 'Certification / Learning Path'}],
 'data analysis': [{'name': 'Google Data Analytics Professional Certificate',
                    'provider': 'Google',
                    'level': 'Beginner',
                    'category': 'Data Analytics',
                    'url': 'https://grow.google/certificates/data-analytics/',
                    'estimated_effort': '8-20 hours',
                    'resource_type': 'Certification / Learning Path'}],
 'data analytics': [{'name': 'Google Data Analytics Professional Certificate',
                     'provider': 'Google',
                     'level': 'Beginner',
                     'category': 'Data Analytics',
                     'url': 'https://grow.google/certificates/data-analytics/',
                     'estimated_effort': '8-20 hours',
                     'resource_type': 'Certification / Learning Path'}],
 'data visualization': [{'name': 'Data Visualization Learning Path',
                         'provider': 'Microsoft Learn',
                         'level': 'Beginner',
                         'category': 'Data Visualization',
                         'url': 'https://www.google.com/search?q=Data+Visualization+Learning+Path+Microsoft+Learn',
                         'estimated_effort': '8-20 hours',
                         'resource_type': 'Certification / Learning Path'}],
 'machine learning': [{'name': 'Machine Learning Specialization',
                       'provider': 'Coursera',
                       'level': 'Intermediate',
                       'category': 'Artificial Intelligence',
                       'url': 'https://www.coursera.org/specializations/machine-learning-introduction',
                       'estimated_effort': '15-40 hours',
                       'resource_type': 'Certification / Learning Path'}],
 'deep learning': [{'name': 'Deep Learning Specialization',
                    'provider': 'DeepLearning.AI',
                    'level': 'Advanced',
                    'category': 'Artificial Intelligence',
                    'url': 'https://www.coursera.org/specializations/deep-learning',
                    'estimated_effort': '30-60 hours',
                    'resource_type': 'Certification / Learning Path'}],
 'artificial intelligence': [{'name': 'AI Engineering Professional Certificate',
                              'provider': 'IBM',
                              'level': 'Intermediate',
                              'category': 'Artificial Intelligence',
                              'url': 'https://www.coursera.org/professional-certificates/ai-engineer',
                              'estimated_effort': '15-40 hours',
                              'resource_type': 'Certification / Learning Path'}],
 'nlp': [{'name': 'Natural Language Processing Specialization',
          'provider': 'DeepLearning.AI',
          'level': 'Intermediate',
          'category': 'Artificial Intelligence',
          'url': 'https://www.coursera.org/specializations/natural-language-processing',
          'estimated_effort': '15-40 hours',
          'resource_type': 'Certification / Learning Path'}],
 'tensorflow': [{'name': 'TensorFlow Developer Learning Path',
                 'provider': 'DeepLearning.AI',
                 'level': 'Intermediate',
                 'category': 'Artificial Intelligence',
                 'url': 'https://www.tensorflow.org/learn',
                 'estimated_effort': '15-40 hours',
                 'resource_type': 'Certification / Learning Path'}],
 'aws': [{'name': 'AWS Certified Cloud Practitioner',
          'provider': 'Amazon Web Services',
          'level': 'Beginner',
          'category': 'Cloud Computing',
          'url': 'https://aws.amazon.com/certification/certified-cloud-practitioner/',
          'estimated_effort': '8-20 hours',
          'resource_type': 'Certification / Learning Path'}],
 'azure': [{'name': 'Microsoft Certified: Azure Fundamentals (AZ-900)',
            'provider': 'Microsoft',
            'level': 'Beginner',
            'category': 'Cloud Computing',
            'url': 'https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/',
            'estimated_effort': '8-20 hours',
            'resource_type': 'Certification / Learning Path'}],
 'google cloud': [{'name': 'Google Cloud Digital Leader',
                   'provider': 'Google Cloud',
                   'level': 'Beginner',
                   'category': 'Cloud Computing',
                   'url': 'https://cloud.google.com/learn/certification/cloud-digital-leader',
                   'estimated_effort': '8-20 hours',
                   'resource_type': 'Certification / Learning Path'}],
 'gcp': [{'name': 'Google Cloud Digital Leader',
          'provider': 'Google Cloud',
          'level': 'Beginner',
          'category': 'Cloud Computing',
          'url': 'https://cloud.google.com/learn/certification/cloud-digital-leader',
          'estimated_effort': '8-20 hours',
          'resource_type': 'Certification / Learning Path'}],
 'cloud computing': [{'name': 'AWS Certified Cloud Practitioner',
                      'provider': 'Amazon Web Services',
                      'level': 'Beginner',
                      'category': 'Cloud Computing',
                      'url': 'https://aws.amazon.com/certification/certified-cloud-practitioner/',
                      'estimated_effort': '8-20 hours',
                      'resource_type': 'Certification / Learning Path'}],
 'docker': [{'name': 'Docker Foundations Professional Certificate',
             'provider': 'Docker',
             'level': 'Beginner',
             'category': 'DevOps',
             'url': 'https://www.docker.com/resources/trainings/',
             'estimated_effort': '8-20 hours',
             'resource_type': 'Certification / Learning Path'}],
 'kubernetes': [{'name': 'Certified Kubernetes Application Developer (CKAD)',
                 'provider': 'Cloud Native Computing Foundation',
                 'level': 'Intermediate',
                 'category': 'DevOps',
                 'url': 'https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/',
                 'estimated_effort': '15-40 hours',
                 'resource_type': 'Certification / Learning Path'}],
 'jenkins': [{'name': 'Jenkins CI/CD Learning Path',
              'provider': 'Jenkins',
              'level': 'Intermediate',
              'category': 'DevOps',
              'url': 'https://www.google.com/search?q=Jenkins+CI%2FCD+Learning+Path+Jenkins',
              'estimated_effort': '15-40 hours',
              'resource_type': 'Certification / Learning Path'}],
 'ci/cd': [{'name': 'DevOps and CI/CD Learning Path',
            'provider': 'Coursera',
            'level': 'Intermediate',
            'category': 'DevOps',
            'url': 'https://www.google.com/search?q=DevOps+and+CI%2FCD+Learning+Path+Coursera',
            'estimated_effort': '15-40 hours',
            'resource_type': 'Certification / Learning Path'}],
 'devops': [{'name': 'DevOps Engineer Professional Certificate',
             'provider': 'IBM',
             'level': 'Intermediate',
             'category': 'DevOps',
             'url': 'https://www.google.com/search?q=DevOps+Engineer+Professional+Certificate+IBM',
             'estimated_effort': '15-40 hours',
             'resource_type': 'Certification / Learning Path'}],
 'terraform': [{'name': 'HashiCorp Certified: Terraform Associate',
                'provider': 'HashiCorp',
                'level': 'Intermediate',
                'category': 'DevOps',
                'url': 'https://developer.hashicorp.com/certifications/infrastructure-automation',
                'estimated_effort': '15-40 hours',
                'resource_type': 'Certification / Learning Path'}],
 'git': [{'name': 'Git and GitHub Learning Path',
          'provider': 'GitHub Skills',
          'level': 'Beginner',
          'category': 'Development Tools',
          'url': 'https://skills.github.com/',
          'estimated_effort': '8-20 hours',
          'resource_type': 'Certification / Learning Path'}],
 'github': [{'name': 'GitHub Foundations',
             'provider': 'GitHub',
             'level': 'Beginner',
             'category': 'Development Tools',
             'url': 'https://resources.github.com/learn/certifications/',
             'estimated_effort': '8-20 hours',
             'resource_type': 'Certification / Learning Path'}],
 'linux': [{'name': 'Linux Essentials',
            'provider': 'Linux Professional Institute',
            'level': 'Beginner',
            'category': 'Operating Systems',
            'url': 'https://www.lpi.org/our-certifications/linux-essentials-overview/',
            'estimated_effort': '8-20 hours',
            'resource_type': 'Certification / Learning Path'}],
 'cybersecurity': [{'name': 'Google Cybersecurity Professional Certificate',
                    'provider': 'Google',
                    'level': 'Beginner',
                    'category': 'Cybersecurity',
                    'url': 'https://grow.google/certificates/cybersecurity/',
                    'estimated_effort': '8-20 hours',
                    'resource_type': 'Certification / Learning Path'}],
 'networking': [{'name': 'Cisco Certified Support Technician - Networking',
                 'provider': 'Cisco',
                 'level': 'Beginner',
                 'category': 'Networking',
                 'url': 'https://www.cisco.com/site/us/en/learn/training-certifications/training/courses/ccst-networking.html',
                 'estimated_effort': '8-20 hours',
                 'resource_type': 'Certification / Learning Path'}],
 'network security': [{'name': 'Cybersecurity Learning Path',
                       'provider': 'Cisco Networking Academy',
                       'level': 'Intermediate',
                       'category': 'Cybersecurity',
                       'url': 'https://www.google.com/search?q=Cybersecurity+Learning+Path+Cisco+Networking+Academy',
                       'estimated_effort': '15-40 hours',
                       'resource_type': 'Certification / Learning Path'}],
 'react': [{'name': 'Meta Front-End Developer Professional Certificate',
            'provider': 'Meta',
            'level': 'Intermediate',
            'category': 'Web Development',
            'url': 'https://www.coursera.org/professional-certificates/meta-front-end-developer',
            'estimated_effort': '15-40 hours',
            'resource_type': 'Certification / Learning Path'}],
 'node.js': [{'name': 'Node.js Application Development Learning Path',
              'provider': 'IBM',
              'level': 'Intermediate',
              'category': 'Web Development',
              'url': 'https://www.google.com/search?q=Node.js+Application+Development+Learning+Path+IBM',
              'estimated_effort': '15-40 hours',
              'resource_type': 'Certification / Learning Path'}],
 'html': [{'name': 'HTML and CSS Web Development',
           'provider': 'Meta',
           'level': 'Beginner',
           'category': 'Web Development',
           'url': 'https://www.google.com/search?q=HTML+and+CSS+Web+Development+Meta',
           'estimated_effort': '8-20 hours',
           'resource_type': 'Certification / Learning Path'}],
 'css': [{'name': 'HTML and CSS Web Development',
          'provider': 'Meta',
          'level': 'Beginner',
          'category': 'Web Development',
          'url': 'https://www.google.com/search?q=HTML+and+CSS+Web+Development+Meta',
          'estimated_effort': '8-20 hours',
          'resource_type': 'Certification / Learning Path'}],
 'mysql': [{'name': 'MySQL Database Learning Path',
            'provider': 'Oracle',
            'level': 'Beginner',
            'category': 'Database',
            'url': 'https://dev.mysql.com/learn/',
            'estimated_effort': '8-20 hours',
            'resource_type': 'Certification / Learning Path'}],
 'mongodb': [{'name': 'MongoDB Developer Learning Path',
              'provider': 'MongoDB University',
              'level': 'Beginner',
              'category': 'Database',
              'url': 'https://learn.mongodb.com/',
              'estimated_effort': '8-20 hours',
              'resource_type': 'Certification / Learning Path'}],
 'communication': [{'name': 'Improving Communication Skills',
                    'provider': 'Coursera',
                    'level': 'Beginner',
                    'category': 'Soft Skills',
                    'url': 'https://www.coursera.org/learn/wharton-communication-skills',
                    'estimated_effort': '8-20 hours',
                    'resource_type': 'Certification / Learning Path'}],
 'communication skills': [{'name': 'Improving Communication Skills',
                           'provider': 'Coursera',
                           'level': 'Beginner',
                           'category': 'Soft Skills',
                           'url': 'https://www.coursera.org/learn/wharton-communication-skills',
                           'estimated_effort': '8-20 hours',
                           'resource_type': 'Certification / Learning Path'}],
 'project management': [{'name': 'Google Project Management Professional Certificate',
                         'provider': 'Google',
                         'level': 'Beginner',
                         'category': 'Management',
                         'url': 'https://grow.google/certificates/project-management/',
                         'estimated_effort': '8-20 hours',
                         'resource_type': 'Certification / Learning Path'}],
 'agile': [{'name': 'Agile Project Management',
            'provider': 'Google',
            'level': 'Beginner',
            'category': 'Management',
            'url': 'https://www.google.com/search?q=Agile+Project+Management+Google',
            'estimated_effort': '8-20 hours',
            'resource_type': 'Certification / Learning Path'}],
 'digital marketing': [{'name': 'Google Digital Marketing & E-commerce Professional Certificate',
                        'provider': 'Google',
                        'level': 'Beginner',
                        'category': 'Marketing',
                        'url': 'https://grow.google/certificates/digital-marketing-ecommerce/',
                        'estimated_effort': '8-20 hours',
                        'resource_type': 'Certification / Learning Path'}],
 'fastapi': [{'name': 'FastAPI Official Tutorial',
              'provider': 'FastAPI',
              'level': 'Beginner to Intermediate',
              'category': 'Backend Development',
              'url': 'https://fastapi.tiangolo.com/tutorial/',
              'estimated_effort': '8-15 hours',
              'resource_type': 'Official Learning Path'}],
 'rest api': [{'name': 'REST API Design Learning Path',
               'provider': 'Microsoft Learn',
               'level': 'Beginner to Intermediate',
               'category': 'API Development',
               'url': 'https://learn.microsoft.com/en-us/training/',
               'estimated_effort': '8-20 hours',
               'resource_type': 'Learning Path'}],
 'scikit-learn': [{'name': 'Scikit-learn User Guide & Tutorials',
                   'provider': 'Scikit-learn',
                   'level': 'Beginner to Intermediate',
                   'category': 'Machine Learning',
                   'url': 'https://scikit-learn.org/stable/user_guide.html',
                   'estimated_effort': '12-25 hours',
                   'resource_type': 'Official Learning Path'}],
 'pytorch': [{'name': 'PyTorch Tutorials',
              'provider': 'PyTorch',
              'level': 'Beginner to Intermediate',
              'category': 'Artificial Intelligence',
              'url': 'https://pytorch.org/tutorials/',
              'estimated_effort': '12-30 hours',
              'resource_type': 'Official Learning Path'}],
 'mlops': [{'name': 'Machine Learning Operations (MLOps) Learning Path',
            'provider': 'Google Cloud',
            'level': 'Intermediate',
            'category': 'MLOps',
            'url': 'https://cloud.google.com/learn/training/machinelearning-ai',
            'estimated_effort': '20-40 hours',
            'resource_type': 'Learning Path'}]}


SKILL_ALIASES = {'ml': 'machine learning',
 'ai': 'artificial intelligence',
 'powerbi': 'power bi',
 'power-bi': 'power bi',
 'ms excel': 'excel',
 'microsoft excel': 'excel',
 'amazon web services': 'aws',
 'microsoft azure': 'azure',
 'google cloud platform': 'google cloud',
 'k8s': 'kubernetes',
 'continuous integration': 'ci/cd',
 'continuous deployment': 'ci/cd',
 'continuous integration/continuous deployment': 'ci/cd',
 'nodejs': 'node.js',
 'reactjs': 'react',
 'react.js': 'react',
 'cyber security': 'cybersecurity'}


def normalize_skill(skill):
    if not isinstance(skill, str):
        return ""

    skill_key = skill.lower().strip()

    return SKILL_ALIASES.get(
        skill_key,
        skill_key
    )


def create_fallback_recommendation(skill):
    """
    Safe fallback for skills without a curated certificate mapping.

    We deliberately label this as a Learning Path instead of inventing
    an unverified certification.
    """
    pretty_skill = skill.strip().title()

    search_url = (
        "https://www.google.com/search?q="
        + quote_plus(
            f"official {pretty_skill} course certification learning path"
        )
    )

    return [
        {
            "name": f"{pretty_skill} Learning Path",
            "provider": "Curated Web Search",
            "level": "Beginner to Intermediate",
            "category": "Skill Development",
            "url": search_url,
            "estimated_effort": "10-30 hours",
            "resource_type": "Learning Path",
            "is_fallback": True
        }
    ]


def recommend_certificates(
    missing_skills,
    required_skills=None,
    preferred_skills=None
):
    recommendations = []

    required_skills = required_skills or []
    preferred_skills = preferred_skills or []

    normalized_required = {
        normalize_skill(skill)
        for skill in required_skills
    }

    normalized_preferred = {
        normalize_skill(skill)
        for skill in preferred_skills
    }

    already_added = set()

    for skill in missing_skills:
        if not isinstance(skill, str):
            continue

        skill_key = normalize_skill(skill)

        if not skill_key or skill_key in already_added:
            continue

        already_added.add(skill_key)

        if skill_key in normalized_required:
            priority = "High"
            skill_type = "Required"
            reason = (
                f"{skill} is a required skill for this opportunity "
                "but was not detected in the candidate profile."
            )

        elif skill_key in normalized_preferred:
            priority = "Medium"
            skill_type = "Preferred"
            reason = (
                f"{skill} is a preferred skill for this opportunity "
                "and could strengthen the candidate's profile."
            )

        else:
            priority = "Medium"
            skill_type = "Skill Gap"
            reason = (
                f"{skill} was identified as a skill gap "
                "for this opportunity."
            )

        certificates = CERTIFICATE_MAP.get(
            skill_key
        )

        if not certificates:
            certificates = create_fallback_recommendation(
                skill
            )

        recommendations.append({
            "skill": skill,
            "skill_type": skill_type,
            "priority": priority,
            "reason": reason,
            "certificates": certificates
        })

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }

    recommendations.sort(
        key=lambda item:
            priority_order.get(
                item["priority"],
                3
            )
    )

    return recommendations
