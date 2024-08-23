# app.py
import streamlit as st
import pandas as pd
from models import Author, Book, session, create_tables
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Create database tables
create_tables()

st.title("Book and Author Data Import")

# File uploader for Excel file
uploaded_file = st.file_uploader("Upload Excel file", type=['xls', 'xlsx'])

if uploaded_file is not None:
    # Read the Excel file using pandas
    try:
        data = pd.read_excel(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(data)
        
        # Confirm button
        if st.button("Confirm Upload"):
            # Validate and insert data into the database
            error_message = ""
            for _, row in data.iterrows():
                try:
                    # Extracting data from the Excel sheet
                    author_name = row['Author Name']
                    email = row['Email']
                    dob = pd.to_datetime(row['Date of Birth']).date()
                    book_name = row['Book Name']
                    isbn_code = row['ISBN Code']
                    
                    # Check if author already exists
                    author = session.query(Author).filter_by(email=email).first()
                    if not author:
                        # Create a new author
                        author = Author(name=author_name, email=email, date_of_birth=dob)
                        session.add(author)
                        session.commit()
                    
                    # Create the book entry
                    book = Book(name=book_name, isbn_code=isbn_code, author_id=author.id)
                    session.add(book)
                    session.commit()
                
                except IntegrityError:
                    session.rollback()
                    error_message += f"Duplicate ISBN Code: {isbn_code}. Data not saved for this record.\n"
                except Exception as e:
                    session.rollback()
                    error_message += f"Error saving record: {str(e)}\n"
            
            if error_message:
                st.error(error_message)
            else:
                st.success("Data uploaded successfully!")
    
    except Exception as e:
        st.error(f"Failed to process the file: {str(e)}")
