create database project;

use project

 CREATE TABLE students_master (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    dob DATE,
    gender VARCHAR(10),
    state VARCHAR(50),
    verification_token VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE
); 


CREATE TABLE pending_users (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    dob DATE,
    gender VARCHAR(10),
    state VARCHAR(50),
    verification_token VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 

CREATE table mentors_master(
	mentor_id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    age VARCHAR(50) not null,
    gender enum('Male','Female','Other'),
    qualification enum('college student','bachelor','masters','M.phill','Phd','others'),
    years_of_experience VARCHAR(50) not null,
    biography text not null,
    is_approved tinyint(1) default 0 
    );
alter table mentors_master add column field_of_work varchar(255);
use project
alter table mentors_master ADD COLUMN image VARCHAR(255);

create table parents_master(
parent_id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) not null,
    lastname VARCHAR(50) not null,
    email VARCHAR(100) UNIQUE not null,
    password VARCHAR(255) not null,
     age varchar(80) not null,adminmentors_masterparents_masterparents_master
    gender VARCHAR(10)not null,
    state VARCHAR(50) not null
    );

create table admin(
id INT AUTO_INCREMENT PRIMARY KEY,
username varchar(255) not null,
email VARCHAR(100) UNIQUE not null,
password VARCHAR(255) not null
);
INSERT INTO admin (username, email, password) VALUES ('admin', 'admin@gmail.com', 'admin');
CREATE TABLE student_mentor_map  (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    mentor_id INT NOT NULL,
    status ENUM('pending', 'accepted', 'declined') DEFAULT 'pending',
    FOREIGN KEY (student_id) REFERENCES students_master(student_id),
    FOREIGN KEY (mentor_id) REFERENCES mentors_master(mentor_id)
)
create table skill_courses( skill_course_id INT AUTO_INCREMENT PRIMARY KEY, skill_course_name varchar(100) NOT NULL , course_description TEXT NOT NULL 
  );
  
  INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('Aerospace and Aviation', 
'This field focuses on building, fixing, and managing airplanes and airports. It also includes exciting technologies like drones and learning how to make air travel safe and efficient.' 
 );

 INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('Agriculture',
'Agriculture is all about growing food and crops. Modern farming uses smart technology and eco-friendly methods to produce food faster while protecting the environment.'
  );

INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('Apparel, Madeups & Home Furnishing',
'This sector involves creating stylish clothes, cozy bedsheets, and decorative items for homes. It’s about designing and making things that combine fashion and comfort.'
 );

INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('Automotive',
'This sector is all about vehicles like cars, bikes, and even electric cars. It includes designing, building, and maintaining vehicles, as well as creating new eco-friendly transportation solutions'
);


INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ( 'Electronics',
'Learn how gadgets and devices like phones and TVs are made. Explore how circuits, chips, and advanced tech work together to make life easier.' 
);



INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('Employability Enhancer',
'Gain essential skills like communication, teamwork, and problem-solving to prepare for future jobs in any field.'
  );



INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('Food Industry Capacity',
'Discover how food is made, processed, and packaged to ensure it’s fresh, tasty, and safe for everyone.'
  );



INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('Furniture and Fittings',
'Learn how furniture and home items are designed and built with creativity, style, and practicality in mind.'
  );


INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('Green Jobs',
'Work towards protecting the planet by learning about renewable energy, waste management, and eco-friendly projects.'
  );


INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('Handicrafts and Carpet',
'Explore traditional art and skills for creating beautiful handmade items like carpets and decorative crafts.' 
 );


INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('Healthcare',
'Learn about how doctors, nurses, and scientists work to improve health and develop medicines to save lives'
);



INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('IT-ITeS (Information Technology and IT-enabled Services)',
'Dive into the world of computers, coding, and technology to build websites, apps, and advanced tech solutions'
);


INSERT INTO skill_courses  ( skill_course_name , course_description   )
VALUES ('Textile',
'Discover how clothes and fabrics are made. Learn about designing, weaving, and producing textiles, a field that provides many job opportunities and contributes to the fashion industry.'
);


CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);


CREATE TABLE course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    about TEXT,
    eligibility TEXT,
    why_choose TEXT,
    FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE
);

INSERT INTO category (category_name) 
VALUES ('Engineering');

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(1, 
 'B.Tech Computer Science Engineering', 
 'BTech CSE is a 4-year UG course that studies practical and theoretical knowledge of computer hardware and software. This course lays emphasis on the basics of computer programming and networking while also comprising a plethora of topics. The admission process for the B.tech CSE is to clear entrance exams such as JEE at a national or state level.', 
 'Candidates aspiring for the B Tech CSE course, need to qualify through their 10+2 exams from a recognized educational institute. Having a science stream in 12th standards is mandatory with Physics, Chemistry and Mathematics as compulsory subjects.', 
 'Students who aspire to pursue a career in the Computer Science field can pursue this program. Students interested in software development, troubleshooting problems, and creating software that can be used must surely go for this degree. Students who aspire to explore the programming field and desire expertise in computer science engineering can pursue this program. Students interested in Maths and Formulas must go for BTech CSE. Students must have attention to detail to study BTech CSE. The demand for Computer Science Engineers is very high.'
);
INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(1, 
 'B.Tech Mechanical Engineering', 
 'BTech Mechanical Engineering is a 4-year undergraduate engineering degree course. This course prepares the students to become Mechanical Engineers. The objective of this course is to prepare students to apply the principles of mechanical engineering for designing, manufacturing, and maintenance of mechanical systems.', 
 'Student must have cleared their 10+2 level examinations with Physics, Chemistry and Mathematics as compulsory subjects. The qualifying aggregate score required in Class 12 is at least 50% and above. Candidates having a 3-year Diploma in the related field from a recognized university are eligible to apply for Lateral Entry admissions.', 
 'Mechanical engineering is one of the oldest fields of engineering. It is the science that forms the principles of Engineering, Physics, and Materials Science for the design, analysis, manufacturing, and maintenance of mechanical systems. Mechanical engineers design everything from new batteries, athletic equipment, and medical devices to personal computers, air conditioners, and automobile engines. Career opportunities in Mechanical Engineering have been immense since its inception.'
);
INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(1, 
 'B.Tech Electrical Engineering', 
 'BTech in Electrical Engineering is a 4-year engineering course that deals with the study of electricity, electromagnetism, and the maintenance and development of electrical equipment. BTech EE also has various electives like Power Systems, Robotics, and Control Systems, Power Electronics, and Artificial Intelligence.', 
 'Students should complete their 10+2 or equivalent examination from a reputed board having PCM as their main subject. They must acquire a minimum of 55% in their higher secondary board examination. For lateral entry students, they must complete their 3-year diploma in a related subject from a recognized board.', 
 'Nowadays, most devices are electricity-based, and electricity is getting more popular because it is eco-friendly. The market for electronic goods is increasing, hence expanding opportunities for electrical engineers. Advancements in technology and AI have further expanded the opportunities. The course provides a basic understanding of engineering concepts and Electrical engineering applications.'
);

INSERT INTO category (category_name) 
VALUES ('Arts');


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(2,
'BA ENGLISH',
'B.A. English is a 3-year UG Course that deals with the various parts of English as a language, both written and spoken. 
BA English admissions take place on the basis of merit of the student’s 12th standard marks obtained. 
Some institutes do hold entrance examinations to admit students. 
BA English is an excellent choice for careers in teaching, media, and advertising, writing, and publishing.',
'10+2 or its equivalent ',
'Choosing a BA in English is ideal if you are passionate about language, literature, and communication. It develops critical thinking, writing, and analytical skills that are highly valued in various careers. This degree opens doors to diverse fields such as media, education, publishing, and content creation. It fosters creativity and cultural awareness by exploring a wide range of texts and perspectives. Moreover, it provides a strong foundation for advanced studies or specialized roles like teaching, editing, or professional writing.'
);


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(2,
'BA Sociology',
'BA Sociology is a 3 year undergraduate course that deals with the study of society like social interaction, social satisfaction, social relations etc. BA Sociology Syllabu includes subjects on collective behavior, cultural Sociology, applied Sociology, etc. BA Sociology is the most preferred undergraduate degree to pursue a Career as a Sociologist, social worker, or counselor. Candidates can pursue the BA Sociology course from Christ University, Delhi University, etc. BA Sociology Admission 2024 is done based on merit and through entrance exams for some colleges. BA Sociology Admission at Delhi University is done based on the CUET entrance exam.',
'A minimum of 50% in Class 10+2 in any stream',
'BA Sociology is the most preferred degree to pursue a career as sociologist, social worker, counselor as per recruiters.The employment opportunities for sociologists is predicted to increase by 4% from 2019-2029, as per US Bureau of Labour Statistics reports, which is fast as compared to many occupations.Sociologists earn up to INR 7 lakhs per year. Human resource manager is the highest paid job after BA Sociology with an average salary of INR 8,32,500 in India.Sociologists have the opportunity to work in NGOs, several welfare organizations, and work in non-traditional roles.BA Sociology also provides excellent preparation for students planning to pursue professional, MA/MS, and/or PhD degrees in business, development studies, law, psychology, Sociology, urban planning, and other social sciences.'
);

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(2,
'BA Political Science',
'BA Political Science or Bachelor of Arts in Political Science is a 3-year undergraduate program. The course involves the study of both national and international political systems. During the course, students are taught historical and modern political systems, public administration, governmental policies and procedures, international relations, and public affairs.',
'The student should have cleared their senior secondary examination with at least 50% marks from a recognized board.',
'The course imparts in-depth knowledge about the various dimensions of political science like the study of government, law & order, socio-economic practices, etc..
Students can find lucrative job offers in the government sector.
The course opens up exciting career opportunities in various fields like Federal, state, and local governments, Law, Business and international organizations, Nonprofit associations and organizations, Electoral politics and polling, Journalism, Research, and teaching.
Apart from seeking jobs, students who choose to pursue BA Political Science can further opt-out for higher education in the related field. Either way, their knowledge of the subject builds up.
The course is a blessing for the students who aim to crack the civil services examination. The course helps them cover a major part of the entrance syllabus.'
);



INSERT INTO category (category_name) 
VALUES ('Science');
INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(3,
'Bachelor of Science in Hotel Management',
'Bachelor of Science in Hotel Management is a 3-year undergraduate program that provides knowledge on how the hotels are run, the management, hotel administration, and skills to attend to the customer.',
'Student  must have passed class 10+2 with a minimum score of 50% from a recognized board.',
'The growing speed of the hotel industry is giving ample job opportunities and hence the candidate can choose a career of their choice.
The exposure of the candidate on a global level helps them in developing their personality. They even gain exposure to the field of Science along with Hotel Management.
The candidates gain valuable knowledge of Sales and Marketing, Tourism and Computer Science.
The candidates get a clear idea of how to set up hotels and entrepreneurship. They can have hotel startups more easily as compared to others.
Being a fancy job, the pay scale for the graduates of this field is high. They get jobs at big foundations.
They can further pursue post-graduation, diploma, or administration courses for a better future.'
);
INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(3,
'BSc Cardiovascular Technology',
'BSc Cardiovascular Technology is a 3-year degree program that deals with diagnosing and monitoring diseases related to the heart and the circulatory system. ',
'10+2 or equivalent with minimum 50% marks in Biology, Chemistry and Physics',
'With more and more people suffering from heart diseases because of many factors including lifestyle, genetics and environment, the importance of this field of study is ever increasing.
Cardiologists and other heart surgeons greatly depend upon the services and support of cardiovascular technologists and technicians for carrying out various complex procedures on patients suffering from heart ailments.
With congenital heart diseases too on the rise, that is those that are prevalent in patients from birth itself, there is an increased awareness among different walks of people about the risks associated with such heart diseases. This in turn, further brings the field in limelight, as people are more likely to avail the services of a cardiovascular technologist.
The numerous advances in the medical field in this domain has been a boon for patients and the medical fraternity alike. With rapid advances in the field, the services are getting more and more affordable, with many availing such services.'
);
INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(3,
'BSc Aeronautical Science',
'Bachelor of Science [B.Sc] (Aeronautical Science), commonly referred as BSc Aeronautical Science is a graduation degree of 3 years duration. It is a specialization degree having a spotlight on the laws of motion, air and objects in Air Space. ',
'Students with more than 50% marks at 10+2 level.',
'Aeronautical science is based upon the study of technology of flying machines.
Aeronautical science is concerned with the aerospace and nautical science which is based upon spacecrafts and satellites operating on earth’s surface and airships operating within the earth’s atmosphere respectively.
Aeronautics carries a specialization of engineering and design and maintenance of air crafts.
After graduation in aeronautics, students have the option of further advanced courses in the field such as: M.E. (Aeronautical Engineering), M.Tech. (Aeronautical Engineering), Ph.D. (Aeronautical Engineering).'
);

INSERT INTO category (category_name) 
VALUES ('Management');


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(4,
'Bachelor of Tourism Management',
' Bachelor of Tourism Management is an undergraduate course of 3 years (divided into 6 semesters) in the Travel and Tourism field. A bachelor’s degree in tourism management is a precondition for acquiring in-depth practical and theoretical knowledge in the field of administration and business management.',
'The eligibility criteria that is followed by all BTM Colleges for admission are mentioned below. The college may have special requirements according to their choice but some of the basic eligibility criteria for BTM is mentioned below:

The candidate should pass their 10+2 from a recognized board in any stream (Science, Arts, Commerce) with a minimum 50% marks .
The candidate should have English in 10+2, as a compulsory subject.',
'A degree in Tourism is the perfect gateway option for a person who wants to break the mold of a conventional life and gain valuable skills in the process, all you will need is a love for travel, good organizational skills and enjoy working with people.
A bachelor degree in Tourism management teaches students about business management, marketing fundamentals, human resources, project management, sustainability, cross-cultural awareness and so much more.
Tourism has the potential to make the world a better place by bringing economic benefits to poorer destinations and keeping tourists hotspot flourishing.
A career in tourism is much fun, when you are exposed to new things and meeting people from all over the world every day, life becomes an adventure.
It is the best field of study through which you not only understand the world we live in but also understand ourselves.'
);

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(4,
'Bachelor of Arts (BA) in Hospitality Management ',
'Bachelor of Arts in hospitality management is a course that deals with the necessary knowledge and education related to Hospitality industries such as airlines and hotels to facilitate smooth processes and conduct quality standards while delivering the services.',
'An intermediate degree in any discipline',
'Students can work as hospitality executives in reputed hotel chains and the tourism sector.
They can take up roles as food and beverage assistants or managers to ensure excellent service.
High-paying careers as catering managers involve organizing event services.
Opportunities exist in the healthcare sector, assisting with physical therapy and patient care.
Students can work in tourism, planning itineraries and stays for guests.
They can become entrepreneurs and start independent projects in hospitality and tourism.
Managerial positions in restaurants and prestigious hotels offer significant responsibility.
Roles in exotic resorts involve handling administrative duties with good exposure.
Students can also work as lodging managers in the hospitality industry.'
);


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(4,
'Bachelor of Business Administration',
'Bachelor of Business Administration and it is a 3-year undergraduate degree. BBA is ideal for students interested in exploring careers in Marketing, Sales, Finance, or HR. Students can pursue a general BBA course to gain an overview of management and business or opt for BBA Specializations such as BBA Finance, BBA Marketing, etc. for more selective learning.',
'You must have passed 10+2 from a recognized board with a minimum of 50-60% aggregate marks.
Candidates from all the streams are eligible to apply for BBA Admissions.
You can apply even if you’re awaiting class 12th results.',
'A Bachelor of Business Administration (BBA) equips students with foundational business knowledge and management skills, preparing them for diverse career opportunities.
It fosters leadership and decision-making abilities, crucial for managing businesses and teams effectively.
The degree offers specialization options like marketing, finance, and human resources, allowing students to align studies with career goals.
BBA graduates are in demand in various industries, ensuring good job prospects and potential for high earning.
It provides a solid base for pursuing advanced studies like an MBA, enhancing career growth further.'
);

INSERT INTO category (category_name) 
VALUES ('Commerce');

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(5,
'B.Com Marketing',
'B.Com Marketing is a three-year course. Eligibility for the course is HSC with 45 % aggregate marks.This is a three-year full-time program, spread over five semesters of teaching and final semester of training based on their choice of the streams.',
'HSC with 45 % aggregate marks.',
'A B.Com in Marketing provides a strong foundation in business principles and specialized knowledge in marketing strategies.
It prepares students for diverse roles in advertising, digital marketing, sales, and market research.
The program develops essential skills like communication, consumer behavior analysis, and brand management.
Marketing professionals are in high demand across industries, offering excellent career prospects and growth opportunities.
This degree is a stepping stone for advanced studies or certifications in marketing, enhancing expertise and employability.'
);

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(5,
'BCom Tourism and Travel Management',
'BCom Tourism and Travel Management is a three year full-time undergraduate degree course designed to focus on the financial and economical management of travel and tourism industry.',
'10+2 Examination cleared with minimum aggregate of 50%',
'A B.Com in Tourism and Travel Management combines business principles with insights into the thriving travel and tourism industry.
It opens career opportunities in travel agencies, airlines, resorts, and event management.
The program develops skills in itinerary planning, customer service, and tourism marketing.
With the global growth in travel, it offers excellent job prospects and potential for entrepreneurship.
Students gain exposure to diverse cultures and industries, making it an exciting and dynamic career choice.'
);

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(5,
'B.Com Accountancy',
'BCom Accountancy is a 3 year Bachelors degree with 6 semesters that focuses on accountancy, Finance, Taxation, and Economics with the aim of providing sound knowledge in business and financial matters.',
'A minimum of 45% to 50% is required in (10+2) to be eligible for admission in the course',
'The course explores subjects such as economic, social science, cultural needs and aspects.
It is made sure that they are functioning democratically and also found in rural areas.
This helps to save and protect the member’s interest in this field. A candidate pursuing a career has many options available.
A candidate can decide to study further in the field as the aspect ratio is high and this field is evergreen.The candidates who complete their bachelors degree can opt to work either in the public sector or the private.'
);

INSERT INTO category (category_name) 
VALUES ('Medical');

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(6,
'Bachelor of Ayurvedic Medicine and Surgery',
'Bachelor of Ayurvedic Medicine and Surgery is a 5-year UG medical course. The Central Council of Indian Medicine (CCIM) is the responsible body for the admission and practice of Ayurvedic medicine in India.',
'Passed 10+2 with a minimum aggregate of 50%-60% and PCB as compulsory subjects',
'Students who are interested in the integrated study of Medical Science and Traditional Ayurveda can pursue a BAMS degree course to grow in the field.
Students should have completed their 10+2 with Physics, Chemistry and Biology from a recognized board.
Students who are interested in finding alternative methods for the treatment of diseases.
Students who are looking for high-salary Medical courses other than MBBS. '
);


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(6,
'Bachelor in homeopathic Medicine and Surgery',
'BHMS stands for Bachelor in homeopathic Medicine and Surgery. BHMS course covers the knowledge regarding homeopathic medical system, which involves the treatment of patients with the high dilutions of the homeopathic medicines mainly in liquid and tablet form to enhance body’s natural healing system. BHMS course duration is 5 years and 6 months which includes 1 year of rotatory internship after completing the final examination.',
'To pursue a Bachelor of Homeopathic Medicine and Surgery (BHMS) in India, students must have completed Class 12 with Physics, Chemistry, and Biology as subjects, scoring at least 50% (40% for reserved categories). Additionally, candidates need to qualify for the NEET (National Eligibility cum Entrance Test) exam.',
'Holistic approach: A homeopathy is a holistic approach that takes into consideration naturopathic care and healing arts, Practitioners observe how patients react to their surroundings and how their lifestyle and genetics affect their ailments.
Global Demand: Since this is an approach that is practiced around the globe, homeopathic doctors will find demand everywhere they go.
Payscale: The salary range of a BHMS graduate is generally higher than that of an Ayurvedic doctor. Students can also find ample opportunities in a government hospital.
The difficulty level of studies: The difficulty level of the curriculum is generally lower than that of Ayurvedic studies since students have to learn knowledge-related studies, as well as modern science whereas in BHMS, students need to learn a small portion of modern science.
Scope: The scope of BHMS is certainly more than that of other medical practices. The opportunities are endless since homeopathy is practiced worldwide. Students can even begin their practice.'
);


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(6,
'Bachelor of Physiotherapy',
'BPT course is a 4-year degree program with 6 months of rotatory internship in rehabilitative medicine. This course focuses on employing physical forces like heat, pressure, electricity, etc. to assist the body in healing itself. It is ideal for students who want to pursue a career as a physiotherapist.',
'50% in 10+2 with science as mainstream.',
'Growing Healthcare Demand: A Bachelor of Physiotherapy (BPT) prepares students for a career in the rapidly expanding healthcare sector, addressing the rising need for physiotherapists.
Holistic Patient Care: It equips students with skills to help patients recover from injuries, disabilities, and chronic conditions, improving their quality of life.
Diverse Career Opportunities: Graduates can work in hospitals, rehabilitation centers, sports clinics, or start their own physiotherapy practice.
Specialization and Growth: The field offers opportunities to specialize in areas like sports physiotherapy, neurology, or orthopedics, ensuring career advancement.
Fulfilling Profession: BPT combines science and compassion, offering a rewarding career that positively impacts individuals and communities.'
);


INSERT INTO category (category_name) 
VALUES ('Paramedical');

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(7,
'Bachelor of Medical Laboratory Technology.',
'BMLT, or Bachelor of Medical Laboratory Technology, is a 3-year undergraduate program designed for individuals aspiring to excel in the field of medical laboratory science. This program offers comprehensive training in laboratory diagnostic procedures, equipping students with the skills and knowledge required for analyzing medical specimens and contributing to the diagnosis and treatment of diseases',
'Completion of 10+2 with Physics, Chemistry, and Biology (PCB) or equivalent',
'High Demand in Healthcare: BMLT professionals play a crucial role in diagnosing diseases, making them indispensable in hospitals and diagnostic labs.
Diverse Career Options: Graduates can work in laboratories, research centers, forensic labs, and public health organizations.
Advanced Skill Development: The program provides expertise in modern diagnostic tools and techniques, keeping pace with advancements in medical technology.
Good Salary Potential: With increasing healthcare needs, BMLT offers competitive salaries and job stability.
Scope for Further Studies: Graduates can pursue advanced courses or specializations, opening doors to higher-paying roles and academic careers'
);


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(7,
'BSc in Cardiac Technology',
'Bachelor of Science in cardiac technology is a 3-4 year undergraduate course. Study of cardiac technology helps doctors to diagnose the disarray in the heart. In this course students learn about the heart and circulatory system. After doing this course students tend to know about invasive procedures during case of emergency and also technical knowledge about the cardiovascular system.',
'10+2 in science',
'BSc in cardiac technology provides students with many more job opportunities to develop a good career after completing graduation.
There is a very high demand for the professionals in this field, on an average there are only 4,000 technologists and over 80,000 heart patients. 
Students also go for higher studies in this field. After completing their studies students get various job options like cardiologist, dialysis technician, cardiovascular technologist
There are many companies hiring these professionals like AIIMS, Fortis Healthcare, Manipal Hospital, Max super Specialty Hospital, etc. 
Their salary also varies from company to company and also their professional experience. Average salary in this field with one year experience could be between INR 4,00,000 to INR 5,50,000 per annum.'
);

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(7,
'Bachelor of Science (B.Sc) Neurophysiology Technology',
'B.Sc Neurophysiology Technology in India is a 3 years long full time program inclusive of 6 semesters scheduled 6 months each. Neurophysiology deals with physiology and neuroscience which directly connects with the core study of nervous system functionality.',
'10+2 Passed with physics, chemistry and Biology.',
'Critical Role in Healthcare: Neurophysiology Technology professionals are essential in diagnosing and monitoring neurological disorders like epilepsy and sleep disorders.
Advanced Skillset: The field equips students with expertise in operating cutting-edge diagnostic tools like EEG, EMG, and nerve conduction studies.
Diverse Career Opportunities: Graduates can work in hospitals, research labs, neurodiagnostic centers, or specialize further in neurology.
High Demand: With the rise in neurological conditions globally, neurophysiology technologists are in high demand, offering job security and growth.
Impactful Work: This career allows individuals to contribute significantly to patient care and improved quality of life for those with neurological issues.'
);


INSERT INTO category (category_name) 
VALUES ('Designing');



INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(8,
'BA Fashion Designing',
'It is the study of the creation of unique and original designs in garments, footwear, jewellery, luggage, etc. Fashion Design is related to the study of the creation of designs which includes conversion of artistic talents and creativity in the creation of products of clothing, textiles, jewellery, footwear and other accessories. IIAD, NIFT, Parul university, etc are some of the top colleges offering this course.The course comprises a meticulous study of the market trends and the related fashion.It is a career-oriented study hence the and thus you may be open to the job world after the completion of the course you study.
If you complete this course you are eligible to hire in the following roles:
Merchandiser
Textile Designer
Retail Fashion Consultant
Management Trainee
Garment Sample Coordinator
Knitwear Designer
Assessor/Examiner of Garment Making
Fashion Expert.',
'10+2 or equivalent qualification in any discipline',
'Why need to choose?
Completing a course in the field of Fashion Design makes one eligible and competent enough to open their own fashion house to exhibit their fashion skills. You can be an independent artist.
Course besides satisfying the creative fancies and the materialistic needs of the people, also promises glamour, fame, success and high pay packages to its students.
After the completion of the course, you can also go for further degrees like master’s and then for research degrees.'
);


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(8,
'B.Des Accessory Design',
'B.Des Accessory Design is a full-time bachelors course of four-years duration which deals with the designing of accessories that can be paired with ethnic and modern attire including designing of jewellery, hair accessory, belts, scarves, footwear, bags etc.',
'Passed 10+2 from a recognized board in any stream',
'BDes in Accessory design poses a prestigious job as the demand for the designer accessory is raising the prestige of the occupation is rising as well.
The demand for the Accessory Designer is rising, simultaneously increasing the scope for Accessory Designer. 
Candidates can also go for various private and corporate sector jobs or become an entrepreneur.
The pay package offered varies from INR 4 LPA to INR 15 LPA depending upon the type of job and the company hiring.'
);

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(8,
'B.Des Fashion Communication',
'BDes Fashion Communication is a well-reputed degree in the designing discipline at the undergraduate level. It offers varied specializations in the field of Fashion Designing, Accessory Designing, Interior Designing, Textile Designing and lot more. 
Over the years, the BDes degree has unfolded to offer several design specializations focusing on Multimedia Designing, Graphic Designing, Visual Communication, Game Designing and VFX Design.',
'10+2 with 50% aggregate marks in any stream',
'BDes Fashion Communication provides self-employment opportunities and generates jobs for other regions as well.
The candidates can expect glamour, fame and success and higher salary packages on being successfully qualified. This course will help you build a professional career in the fashion industry.
With this degree, you can easily find jobs abroad like Canada, USA etc.
One can take part in exhibitions and auctions of your creative works that can be organized in various parts of the world.
Candidates get hired as Promotion & Merchandising Officer Fashion Assistant, Fashion Advertiser, Fashion Stylist, Teacher & Lecturer, Fashion Designer, Fashion Journalist, Sales Executive, Fashion Consultant, Area Operations Manager, Fashion Consultant etc.'
);


INSERT INTO category (category_name) 
VALUES ('Hotel Management');

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(9,
'Bachelor of Hotel Management',
'
Bachelor of Hotel Management course is a 3-year undergraduate degree in hospitality management. Few of the colleges and institutes also offer this course for 4-years like WelcomGroup of Hotel Management, Army Institute of Hotel Management and Catering Technology. BHM course is ideal for individuals who have strong communication and interpersonal skills.',
'The aggregate of 50% score in 10+2 from a recognized board or university with English as a mandatory subject',
'Growing Hospitality Industry: Hotel management professionals are in high demand as the global hospitality and tourism sector continues to expand.
Diverse Career Opportunities: Graduates can work in hotels, resorts, restaurants, event management, or start their own hospitality business.
Development of Management Skills: The program equips students with leadership, organizational, and customer service skills essential for managing hospitality operations.
Global Exposure: The hospitality industry offers opportunities to work internationally, experiencing different cultures and work environments.
Lucrative Career Path: With rapid industry growth, hotel management offers high-paying roles and significant career advancement potential.'
);


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(9,
'BSc in Catering Science and Hotel Management',
'BSc in Catering Science and Hotel Management, BSc in Catering Science and Hotel Management is a three-year full-time undergraduate program divided into 6 semesters. The main objective of the hotel management course is to offer experienced applicants the compulsory abilities, knowledge, values, and attitudes to occupy vital operational situations in the hospitality industry.
The Subjects taught while pursuing the BSc in Catering Science and Hotel Management course may vary from one college to the other but few topics are listed below:

Foundation course in food production
Foundation course in food beverage service
Foundation course in the front office
Foundation course accommodation operations
Hotel engineering
Nutrition
Principle of food science
Accountancy
Communication
Management in tourism
Food production processes
Food safety and quality
Financial management
Strategic Management',
'The Candidates who wish to pursue this program must pass 10+2 in the science stream with a minimum of 50% aggregate marks.',
'
The BSc in Catering Science and Hotel Management degree program offers a good base for a higher degree program in corresponding subjects such as a Master’s degree and more. Students can have jobs in hotels as reception for the guests, making room reservations, handling correspondence, preparing bills, and keeping accounts of the guest services being handled at the front office. 

Rest jobs are the effort of keeping the hotel, rooms, bars, and restaurants clean to make it respectable to the guests along with guaranteeing facilities and comfort to them by the department.'
);

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(9,
'BSc Hospitality',
'BSc Hospitality Studies course has been designed to offer the students the knowledge of management of food beverage and accommodation along with general management. 
It provides in-depth laboratory work for students to gain the knowledge and the required skills standard for the functioning of the core departments of any hotel related to food and beverage production and management, catering operations, general management, human resource management, Finance Management, among others.',
'To be eligible for BSc Hospitality Studies course, a candidate must have passed the class 12th exam with a minimum of 50% aggregate from a recognized board. ',
'Diverse opportunities: A graduate degree in Hospitality Services can open up job opportunities for the candidates in various unique profiles such as Hotel Manager, Catering Officer, Hospitality Executive, and many more. 
Higher Education: Candidates after completion of the course can opt for higher education by enrolling them in the MSc programs such as MSc Hospitality Services, MSc in Hospital Administration, MSc in Hospitality and Tourism Management, MSc in Hospitality. 
A PG degree also increases the job prospect for the candidates and thus, the candidates can opt for PhD Courses after completing their PG.
Competitive Salary: A Hospitality Executive in India earns around INR 6,40,000 per annum. The salary increases with experience in this field.'
);


INSERT INTO category (category_name) 
VALUES ('Agriculture');

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(10,
'BSc Agriculture',
'BSc Agriculture is a 3 year UG course providing all the scientific methods and techniques of agriculture. Students after completing BSc in Agriculture have a good scope in their careers. There are many kinds of BSc Agriculture Jobs available like Agricultural Officer, Agricultural Analyst, Plant Breeder, Seed Technologist.',
'50% marks in class 12 in Science (Physics, Chemistry, Biology) stream from a recognized educational board',
'Students interested in the use of technology for agriculture must do this course.
Students must be quick thinking with good analytical skills in order to study BSc Agriculture since agriculture is a very diverse field where quick thinking is a must. 
In the field of agriculture, it is necessary for students to have a good hold over time management since agriculture is a time dominated field.'
);

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(10,
'BSc Horticulture',
'The stream concentrates mainly on crop plants, vegetables, fruits, cereals, and medicinal plants.
It individually discusses various types of crops like fruit crops, vegetable crops, garden crops, plantation crops, and many other types.
The course discusses important topics related to the breeding of plants like the Growth and Development of Horticultural Crops, Seed Production of vegetables, Tuber and Spice Crops, among others',
'10+2 in Science Stream with PCB / PCMB.',
'The Students  willing to join the farming sector will find this course as hugely beneficial. This course will train them to farm various types of crop plants.
The candidates who complete this course will have enough knowledge to pursue any kind of agricultural research in the future. They can develop better seeds, research on breeding conditions and do many more different types of research.
The candidates can work to develop their own farms and Horticulture gardens. They can start their own agricultural businesses.
This course offers a vast opportunity for government jobs. Many government departments and banks offer jobs to BSc Horticulture Science candidates.
Since farming will always be an important sector, candidates with a degree in Horticulture will always be in demand in the job market.'
);


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(10,
'Bachelor of science Agronomy',
'Agronomy involves the science as well as technology that are needed for the growth of plants for the purpose of food, fibres and fuel etc. Agronomy encompasses work in fields such as plant physiology, soil science and plant genetics.

The field of Agriculture makes use of a wide range of techniques as to make their work simpler and easier. With the development of innovative techniques and machinery, the field of agriculture has risen to such a level that not much things affect it as adversely as in the earlier days and the yields of crops are rising too.',
'A candidate shall be eligible for admission to B.Sc. Agronomy, if he or she is physically fit to carry out field work related with agricultural activities.

Students should pass the 10+2 or Intermediate examination in Agriculture or in Science with Physics, Chemistry and Mathematics or Biology or any other equivalent examination recognized by the University.
Obtained at least 50% marks in aggregate. For Scheduled Caste or Scheduled Tribe candidates, the eligibility will be as per University rules.

Candidates appearing at the respective qualifying examinations shall be eligible to appear at the entrance examination but shall have to provide the proof of passing the said examination as and when called for, prior to their admission.',
'The job as well as career opportunities available for students who have accomplished their education in B.Sc. Agronomy are quite high. When one is talking about education, the best choice is to pursue the Master of Science in agronomy course. The master’s degree in this field will enable students get more knowledge about the subject. In addition to this, this will enhance their opportunities to get good jobs.

There are quite a few government as well as private bodies that recruit skilled candidates of this field. Banks, insurance companies and the Animal industry etc. take in professionals from the field of agriculture.'
);

INSERT INTO category (category_name) 
VALUES ('Architucture');

INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(11,
'Bachelor of Architecture (B Arch)',
'
A Bachelor of Architecture (B Arch) equips students with the knowledge and skills needed to design, plan, and oversee the construction of buildings and structures. It combines creativity, technical expertise, and a deep understanding of construction principles, offering diverse career opportunities in architecture, urban planning, and interior design.',
'50% marks in Class 12 or Class 10 + Diploma from a recognized college.',
'Skills Development: B Arch program is a blend of theoretical and practical knowledge which allows students to express design ideas and develop practical skills. 
Fosters new Ideas: The curriculum of top B Arch colleges is meant to foster creativity, innovation and sustain
ability in students.
Lucrative Career Prospects:  Bachelor of Architecture can be both a fulfilling and lucrative career path as companies are flocking in search of skilled architects. The average starting salary after a B Arch degree is INR 3.5 LPA and can go up to INR 15 LPA.
Licensure: After completing the Bachelor of Architecture, students can apply for a license to practice as a professional architect.'
);


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(11,
'B Arch Landscape Architecture',
'B Arch Landscape Architecture involves urban planning, site planning, environmental planning, real estate planning, green infrastructure planning, and many more. Landscape architects work both as lead professionals and as specialist site designers on several projects, including civic developments, urban designing, commercialization, industrial and tourism developments, and residential and lifestyle subdivisions.

Landscape Architecture is subject of both an art and a science, with:

Make space for people.
Using several types of tools of planning, designing, managing, and analysis.
acquiring and guiding the development of land.
building human civilization and natural ecosystems to maintain a healthy and stable environment.
They work in areas of Plant sciences, Planting design techniques, and Garden maintenance and management.',
'Students  should have completed a 10+2 examination or equivalent examination, with Physics, Chemistry, and Mathematics with a minimum of 50% marks.
Candidates who have Cleared different national and state level entrance exams like BITSAT, JEE, etc, are eligible for B Arch Landscape Architecture program in different colleges.
Applicants are also required to clear the National Aptitude Test in Architecture, (NATA) exam which is a body of the Council of Architecture (CoA) conducted by the National Institute of Advanced Studies in Architecture, (NASA) to get admission in B.Arch. Landscape Architecture Course
The candidate age should be minimum of 17. The age limit may vary according to the university criteria.',
'The 5-year course offers a practicing license through the Council of Architecture (COA), a benefit not available in many countries after the same duration.
It provides exposure to local culture and architectural practices.
The curriculum aligns with global standards, similar to courses in other countries.
It is more economical than studying abroad.
India boasts well-established colleges and experienced faculty in the field.'
);


INSERT INTO course (category_id, course_name, about, eligibility, why_choose)
VALUES 
(11,
'BArch Interior Design',
'BArch Interior Design is a creative course study, which mainly focuses on practices of skills needed to designing and constructing the furniture to be used for filling up the interior spaces, construct and apply innovative ideas to the design of malls, houses, commercial buildings, etc, drawing the layouts for efficient usage of the space.
It mainly covers the study of organizing, managing and planning of the interiors of various establishments. The program often combines the study of aspects of architecture, environmental psychology, product design, traditional decoration, fine arts, liberal arts and science & technology courses.',
'10+2 with a minimum aggregate score of 50%.',
'Most of the students prefer to study BArch Interior Design course because of the following advantages:

The course seems to be perfect for candidates with interest in architectural drawings and other design related activities.
Enrolled students would possess many skills such as analytical skills, imagination, creativity, self-motivation, and listening skills. 
BArch Interior Designs graduates salary on an average is estimated to be INR 5 Lakh per annum.
Candidates can opt for various private and government sectors jobs both in India and abroad.'
);



create table life_coach_master(coach_id INT AUTO_INCREMENT PRIMARY KEY,firstname varchar(100) not null,lastname varchar(100) not null,email varchar(100) unique not null,password varchar(100) not null,age varchar(80), gender enum('male','female','others') not null,qualification enum('college student', 'bachelor', 'masters','M.Phill','Ph.D','others'), years_of_experience varchar(80) not null,field_of_work varchar(100), biography TEXT,is_approved TINYINT(1) DEFAULT 0,image VARCHAR(255) DEFAULT NULL);

CREATE TABLE student_life_coach_map  (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    coach_id INT NOT NULL,
    status ENUM('pending', 'accepted', 'declined') DEFAULT 'pending',
    FOREIGN KEY (student_id) REFERENCES students_master(student_id),
    FOREIGN KEY (coach_id) REFERENCES life_coach_master(coach_id)
); 


use project

-- Create the questions table
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(255) NOT NULL
);

-- Create the answers table
CREATE TABLE IF NOT EXISTS answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT,
    text VARCHAR(255) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);

-- Insert sample questions
INSERT INTO questions (text) VALUES
    ('Which of the following courses prepares students for careers in fashion design?'),
    ('Which course is best for someone interested in software development?'),
    ('Which program provides skills in photography and video editing?'),
    ('Which of these courses is related to agriculture?'),
    ('What course helps individuals learn about hotel management and hospitality?'),
    ('Which course would help a student interested in teaching young children?'),
    ('Which of the following courses is ideal for pursuing a career in interior design?'),
    ('What type of course is suited for someone interested in automotive repair?'),
    ('Which course specializes in financial planning and wealth management?'),
    ('Which program is designed for someone aiming to build a career in journalism?');

-- Insert answers for each question
-- For the first question
INSERT INTO answers (question_id, text, is_correct) VALUES
    (1, 'Diploma in Fashion Technology', TRUE),
    (1, 'BA in Literature', FALSE),
    (1, 'B.Sc. in Chemistry', FALSE),
    (1, 'MBA in Finance', FALSE);

-- For the second question
INSERT INTO answers (question_id, text, is_correct) VALUES
    (2, 'B.Tech in Computer Science', TRUE),
    (2, 'Diploma in Journalism', FALSE),
    (2, 'Certificate in Event Management', FALSE),
    (2, 'MA in History', FALSE);

-- For the third question
INSERT INTO answers (question_id, text, is_correct) VALUES
    (3, 'Certificate in Media Production', TRUE),
    (3, 'B.Sc. in Physics', FALSE),
    (3, 'Diploma in Accounting', FALSE),
    (3, 'MBA in Marketing', FALSE);

-- For the fourth question
INSERT INTO answers (question_id, text, is_correct) VALUES
    (4, 'B.Sc. in Agriculture', TRUE),
    (4, 'Diploma in Business Management', FALSE),
    (4, 'BA in Sociology', FALSE),
    (4, 'BCA (Bachelor of Computer Applications)', FALSE);

-- For the fifth question
INSERT INTO answers (question_id, text, is_correct) VALUES
    (5, 'Bachelor of Hotel Management', TRUE),
    (5, 'M.Sc. in Biochemistry', FALSE),
    (5, 'Diploma in Urban Planning', FALSE),
    (5, 'Certificate in Wildlife Studies', FALSE);

-- For the sixth question
INSERT INTO answers (question_id, text, is_correct) VALUES
    (6, 'Diploma in Early Childhood Education', TRUE),
    (6, 'B.Tech in Mechanical Engineering', FALSE),
    (6, 'BA in Economics', FALSE),
    (6, 'M.Com in Finance', FALSE);

-- For the seventh question
INSERT INTO answers (question_id, text, is_correct) VALUES
    (7, 'Diploma in Interior Design', TRUE),
    (7, 'B.Sc. in Biology', FALSE),
    (7, 'Certificate in Public Speaking', FALSE),
    (7, 'MBA in Operations Management', FALSE);

-- For the eighth question
INSERT INTO answers (question_id, text, is_correct) VALUES
    (8, 'Certificate in Automobile Mechanics', TRUE),
    (8, 'B.Sc. in Environmental Science', FALSE),
    (8, 'Bachelor of Arts in History', FALSE),
    (8, 'M.Tech in Civil Engineering', FALSE);

-- For the ninth question
INSERT INTO answers (question_id, text, is_correct) VALUES
    (9, 'Diploma in Financial Planning', TRUE),
    (9, 'BA in Political Science', FALSE),
    (9, 'Certificate in Fitness Training', FALSE),
    (9, 'B.Sc. in Physics', FALSE);

-- For the tenth question
INSERT INTO answers (question_id, text, is_correct) VALUES
    (10, 'Bachelor of Mass Communication', TRUE),
    (10, 'Diploma in Machine Learning', FALSE),
    (10, 'B.Tech in Electronics', FALSE),
    (10, 'Certificate in Culinary Arts', FALSE);


CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL, -- Can be a student or mentor
    receiver_id INT NOT NULL, -- Can be a student or mentor
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES students_master(student_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES mentors_master(mentor_id) ON DELETE CASCADE
);

