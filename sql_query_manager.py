import re
import logging

class SQLQueryInspector:
    def __init__(self, query):
        self.query = query
        self.logger = self._setup_logger()
        self.issues = []

    def _setup_logger(self):
        logger = logging.getLogger("sql_query_inspector")
        logger.setLevel(logging.INFO)

        # Create a file handler and set the logging level to INFO
        file_handler = logging.FileHandler("query_inspector.log")
        file_handler.setLevel(logging.INFO)

        # Create a formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        return logger

    def inspect_query(self):
        # Check for SELECT statements
        if not re.match(r'\s*SELECT', self.query, re.IGNORECASE):
            self.issues.append("Only SELECT statements are allowed.")

        # Check for potential SQL injection
        if re.search(r'\bDROP\b|\bDELETE\b|\bTRUNCATE\b|\bUPDATE\b|\bINSERT\b', self.query, re.IGNORECASE):
            self.issues.append("Potential SQL injection detected.")

        # Check for unsafe keywords
        unsafe_keywords = ['xp_cmdshell', 'exec', 'sp_', 'xp_', ';\s*--']
        for keyword in unsafe_keywords:
            if re.search(fr'\b{keyword}\b', self.query, re.IGNORECASE):
                self.issues.append(f"Potentially unsafe SQL keyword '{keyword}' detected.")

        # Check for use of wildcard (*)
        if re.search(r'\*\s*FROM', self.query):
            self.issues.append("Avoid using wildcard (*) in SELECT queries. Specify column names explicitly.")

        # Check for use of LIMIT/OFFSET without ORDER BY
        if re.search(r'\bLIMIT\b|\bOFFSET\b', self.query, re.IGNORECASE) and not re.search(r'\bORDER\s+BY\b', self.query, re.IGNORECASE):
            self.issues.append("Use of LIMIT/OFFSET without ORDER BY may result in unpredictable results.")

        # Check for use of semicolons in the middle of the query
        if re.search(r';(?!\s*--)', self.query):
            self.issues.append("Avoid the use of semicolons (;) in the middle of the query. It can lead to unexpected behavior.")

        # Check for use of dynamic SQL
        if re.search(r'\bEXEC\b|\bEXECUTE\b', self.query, re.IGNORECASE):
            self.issues.append("Avoid using dynamic SQL. Consider using parameterized queries.")

        # Check for use of JOIN without ON clause
        if re.search(r'\bJOIN\s+[^\s]+(?!\s+ON\b)', self.query, re.IGNORECASE):
            self.issues.append("Use of JOIN without an ON clause may result in a Cartesian product. Specify the join conditions.")

        # Check for use of UNION without matching column count
        if re.search(r'\bUNION\b', self.query, re.IGNORECASE):
            union_counts = re.findall(r'\bSELECT\b.*?\bFROM\b.*?(\bUNION\b|$)', self.query, re.IGNORECASE)
            if len(set(map(lambda x: x.count(','), union_counts))) > 1:
                self.issues.append("UNION queries must have matching column counts in each SELECT statement.")

        # Encourage the use of parameterized queries
        if re.search(r':\w+', self.query):
            self.issues.append("Encouragement: Consider using parameterized queries for enhanced security.")

        if self.issues:
            # Log detected issues
            self.logger.warning("Detected issues in SQL query:\n%s", "\n".join(self.issues))
            print("Detected issues in SQL query:\n", "\n".join(self.issues))
        else:
            # No issues, return the output query
            return self.query

if __name__ == "__main__":
    # Example usage
    sql_query = "SELECT * FROM users WHERE username = 'admin'; DROP TABLE users;"
    inspector = SQLQueryInspector(sql_query)
    output_query = inspector.inspect_query()

    # If there are no issues, print or use the output query
    if output_query:
        print("Output query:", output_query)
