import click
import os
from github_code_assistant import GitHubCodeAssistant
from dotenv import load_dotenv
import json

load_dotenv()

@click.group()
def cli():
    """GitHub Code Assistant CLI"""
    pass

@cli.command()
@click.option('--repo', prompt='Repository (owner/name)', help='Repository in format owner/name')
@click.option('--path', prompt='File path', help='Path to the file')
def read_file(repo, path):
    """Read a file from the repository"""
    assistant = GitHubCodeAssistant(repo)
    content = assistant.read_file(path)
    click.echo(content)

@cli.command()
@click.option('--repo', prompt='Repository (owner/name)', help='Repository in format owner/name')
@click.option('--path', prompt='File path', help='Path to the file')
@click.option('--content', prompt='File content', help='Content to write')
@click.option('--message', prompt='Commit message', help='Commit message')
def write_file(repo, path, content, message):
    """Write content to a file"""
    assistant = GitHubCodeAssistant(repo)
    result = assistant.write_file(path, content, message)
    click.echo(f"File {'updated' if result else 'not updated'}")

@cli.command()
@click.option('--repo', prompt='Repository (owner/name)', help='Repository in format owner/name')
@click.option('--title', prompt='PR title', help='Pull request title')
@click.option('--body', prompt='PR body', help='Pull request body')
@click.option('--branch', prompt='Branch name', help='Branch name')
def create_pr(repo, title, body, branch):
    """Create a pull request"""
    assistant = GitHubCodeAssistant(repo)
    pr = assistant.create_pull_request(title, body, branch)
    click.echo(json.dumps(pr, indent=2))

@cli.command()
@click.option('--repo', prompt='Repository (owner/name)', help='Repository in format owner/name')
@click.option('--path', default="", help='Directory path (optional)')
def list_files(repo, path):
    """List files in a directory"""
    assistant = GitHubCodeAssistant(repo)
    files = assistant.list_files(path)
    click.echo(json.dumps(files, indent=2))

if __name__ == '__main__':
    cli()