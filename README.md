# Note search tool

This tool works with a strictly defined directory structure and README.md files

# Add note-search binary to path

Run the following script: 
"""
(echo; echo '# Add note-search binary to path') >> $HOME/.bash_profile
(echo 'PATH=\"~/w/note-search/bin/:${PATH}') >> $HOME/.bash_profile
"""

And restart shell. This assumes note-search is located in ~/w