#!/usr/bin/env python3
"""
Data Analysis Agent - Main Application
"""

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from core.data_loader import load_dataset, generate_schema
from tools.analysis_tool import set_global_data
from tools.suggestion_tool import suggestion_tool
from agents.agent_manager import create_agent
from utils.file_handlers import setup_output_directory

def main():
    """Main application entry point."""
    print("Data Analysis Agent")
    print("=" * 50)
    
    # Setup output directory
    setup_output_directory()
    
    # Load dataset
    global_df = None
    attempts = 0
    while True:
        path = input("Enter dataset path (or 'exit' to quit): ").strip()
        if path.lower() in ["exit", "quit"]:
            return
        
        try:
            global_df = load_dataset(path)
            schema = generate_schema(global_df)
            
            # Set global data for tools
            set_global_data(global_df, schema)
            
            print("Dataset loaded successfully!")
            print("Dataset Schema:", schema)
            print(f"Shape: {global_df.shape}")
            break
        except Exception as e:
            print(f"Error: {e}")
            attempts += 1
    
    # Initialize agent
    try:
        agent = create_agent()
        print("\nAgent initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return
    
    print("\nUsage: Ask questions in natural language or type 'suggestions'")
    
    # Show initial suggestions
    try:
        print(f"\n{suggestion_tool.invoke('')}")
    except Exception as e:
        print(f"Could not generate initial suggestions: {e}")
    
    # Main interaction loop
    while True:
        try:
            user_query = input("\nQuery: ").strip()
            
            if user_query.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_query:
                continue
            
            # Handle special commands
            if user_query.lower() == "suggestions":
                print("\n**Suggested Analyses:**")
                try:
                    print(suggestion_tool.invoke(''))
                except Exception as e:
                    print(f"Error generating suggestions: {e}")
                continue
            
            # Process query with agent
            try:
                result = agent.invoke({"input": user_query})
                print(f"\n{result['output']}")
                print("-" * 50)
            except Exception as e:
                print(f"Error processing query: {str(e)}")
                
        except KeyboardInterrupt:
            print("\nSession ended!")
            break
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")

if __name__ == "__main__":
    main()