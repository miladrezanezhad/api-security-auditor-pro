#!/usr/bin/env python3
"""
Main CLI entry point for API Security Auditor Pro
"""

import asyncio
import sys
import json
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """API Security Auditor Pro - Professional API Security Testing Tool"""
    pass


@cli.command()
@click.argument("url")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--format", "-f", type=click.Choice(["json", "html"]), default="json", help="Output format")
@click.option("--timeout", "-t", type=int, default=30, help="Request timeout in seconds")
def scan(url, verbose, output, format, timeout):
    """Scan a single API endpoint for security vulnerabilities"""
    console.print(f"[bold cyan]🔍 Starting security scan on:[/] {url}")
    
    from ..core.scanner import SecurityScanner
    
    scanner = SecurityScanner(target_url=url, timeout=timeout)
    results = asyncio.run(scanner.run_scan())
    
    # Display results table
    table = Table(title="Security Scan Results")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Severity", style="yellow")
    
    if results.get("vulnerabilities"):
        for vuln in results["vulnerabilities"]:
            table.add_row(
                vuln.get("check", "Unknown"),
                "⚠️ VULNERABLE",
                vuln.get("severity", "MEDIUM")
            )
    else:
        table.add_row("All Checks", "✅ PASSED", "N/A")
    
    console.print(table)
    
    if output:
        with open(output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        console.print(f"[green]✅ Report saved to: {output}[/]")
    
    if results.get("vulnerabilities"):
        console.print(f"\n[red]⚠️ Found {len(results['vulnerabilities'])} vulnerabilities![/]")
        sys.exit(1)
    else:
        console.print("\n[green]✅ No vulnerabilities found![/]")


@cli.command()
@click.argument("url")
@click.option("--requests", "-r", type=int, default=50, help="Number of requests to send")
@click.option("--concurrency", "-c", type=int, default=5, help="Number of concurrent connections")
@click.option("--delay", "-d", type=float, default=0.05, help="Delay between requests in seconds")
def test_rate_limit(url, requests, concurrency, delay):
    """Test rate limiting effectiveness on the API"""
    console.print(f"[bold cyan]🚦 Testing rate limiting on:[/] {url}")
    
    from ..checks.rate_limiting import test_rate_limiting
    
    results = asyncio.run(test_rate_limiting(url, requests, concurrency, delay))
    
    table = Table(title="Rate Limiting Test Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Total Requests", str(results["total_requests"]))
    table.add_row("Successful (200)", str(results["successful"]))
    table.add_row("Rate Limited (429)", str(results["rate_limited"]))
    table.add_row("Errors", str(results["errors"]))
    table.add_row("Rate Limiting Present", "✅ Yes" if results["rate_limited"] > 0 else "❌ No")
    
    console.print(table)
    
    if results["rate_limited"] == 0:
        console.print("\n[yellow]⚠️ Warning: No rate limiting detected![/]")
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def report(input_file, output):
    """Generate report from previous scan results"""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            results = json.load(f)
        
        console.print("[bold cyan]📊 Report Summary[/]")
        console.print(f"Target: {results.get('target', 'N/A')}")
        console.print(f"Scan Time: {results.get('timestamp', 'N/A')}")
        console.print(f"Vulnerabilities Found: {len(results.get('vulnerabilities', []))}")
        
        if output:
            import shutil
            shutil.copy(input_file, output)
            console.print(f"[green]✅ Report saved to: {output}[/]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/]")
        sys.exit(1)


if __name__ == "__main__":
    cli()