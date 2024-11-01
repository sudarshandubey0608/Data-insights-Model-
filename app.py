import os
import sqlite3
import openai
from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Set your OpenAI API key (securely, e.g., using environment variables)
openai.api_key = os.environ.get('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')

def get_schema(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema[table_name] = [column[1] for column in columns]
    conn.close()
    return schema

def query_database(query):
    conn = sqlite3.connect('nba.sqlite')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        conn.close()
        return results, columns
    except Exception as e:
        conn.close()
        return f"Error: {str(e)}", []

def create_chart(df):
    plt.figure()
    df.plot(kind='bar')  # Example: Create a bar chart
    plt.title('Data Visualization')
    plt.xlabel('Index')
    plt.ylabel('Values')
    plt.tight_layout()

    # Save to a PNG in memory
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode('utf8')

def get_sql_query(user_query, schema):
    prompt = f"Database schema: {schema}\nUser query: {user_query}\nGenerate a SQL query to answer the user's question."

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Or another suitable model
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        temperature=0.5
    )

    sql_query = response.choices[0].message.content
    return sql_query.strip()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_query = request.form['query']
        schema = get_schema('nba.sqlite')

        sql_query = get_sql_query(user_query, schema)

        if "Error" in sql_query:
            return sql_query.strip()

        db_response, columns = query_database(sql_query)

        if isinstance(db_response, str):
            return db_response.strip()

        df = pd.DataFrame(db_response, columns=columns)

        if "count" in user_query.lower():
            result = df.iloc[0, 0]
            return f"Number of players: {result}".strip()
        else:
            return render_template('results.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

    