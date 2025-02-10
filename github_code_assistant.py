import os
from github import Github
import base64
from datetime import datetime
import logging
from typing import Dict, List, Optional

class GitHubCodeAssistant:
    def __init__(self, repo_name: str, branch: str = "main"):
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        self.repo = self.github.get_repo(repo_name)
        self.branch = branch
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='code_assistant.log'
        )
        self.logger = logging.getLogger(__name__)

    def read_file(self, file_path: str) -> str:
        """Read file content from GitHub repository"""
        try:
            content = self.repo.get_contents(file_path, ref=self.branch)
            file_content = base64.b64decode(content.content).decode('utf-8')
            self.logger.info(f"Successfully read file: {file_path}")
            return file_content
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {str(e)}")
            raise

    def write_file(self, file_path: str, content: str, commit_message: str) -> bool:
        """Write or update file in GitHub repository"""
        try:
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            full_commit_message = f"{commit_message}\n\nAutomated commit by CodeAssistant at {current_time}"
            
            try:
                # Try to get existing file
                file = self.repo.get_contents(file_path, ref=self.branch)
                self.repo.update_file(
                    file_path,
                    full_commit_message,
                    content,
                    file.sha,
                    branch=self.branch
                )
            except Exception:
                # File doesn't exist, create new
                self.repo.create_file(
                    file_path,
                    full_commit_message,
                    content,
                    branch=self.branch
                )
            
            self.logger.info(f"Successfully wrote to file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error writing to file {file_path}: {str(e)}")
            raise

    def create_pull_request(self, title: str, body: str, head_branch: str) -> Dict:
        """Create a pull request for changes"""
        try:
            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=self.branch
            )
            self.logger.info(f"Created PR #{pr.number}: {title}")
            return {
                "number": pr.number,
                "url": pr.html_url,
                "title": pr.title
            }
        except Exception as e:
            self.logger.error(f"Error creating PR: {str(e)}")
            raise

    def create_branch(self, branch_name: str) -> bool:
        """Create a new branch from current branch"""
        try:
            source = self.repo.get_branch(self.branch)
            self.repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=source.commit.sha
            )
            self.logger.info(f"Created branch: {branch_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating branch {branch_name}: {str(e)}")
            raise

    def list_files(self, path: str = "") -> List[Dict]:
        """List files in a directory"""
        try:
            contents = self.repo.get_contents(path, ref=self.branch)
            files = []
            for content in contents:
                files.append({
                    "name": content.name,
                    "path": content.path,
                    "type": "file" if content.type == "file" else "directory",
                    "size": content.size
                })
            return files
        except Exception as e:
            self.logger.error(f"Error listing files in {path}: {str(e)}")
            raise