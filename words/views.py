from collections import Counter
from django.shortcuts import render, redirect
from .forms import TextReaderForm
from .models import TextReader
from django.http import HttpResponse
import io

def upload_file(request):
    analysis = None
    file_content = None
    word_frequencies = None

    if request.method == 'POST':
        form = TextReaderForm(request.POST, request.FILES)
        if form.is_valid():
            text_file = request.FILES['file']
            content = text_file.read().decode('utf-8')
            
            lines = content.strip().split('\n')
            line_count = len(lines)
            word_count = sum(len(line.split()) for line in lines)
            char_count = len(content)
            
            analysis = form.save(commit=False)
            analysis.lines = line_count
            analysis.words = word_count
            analysis.characters = char_count
            analysis.save()
            
            file_content = content
            
    else:
        form =TextReaderForm()
        
    return render(request, 'upload.html', {'form': form, 'analysis': analysis, 'file_content': file_content})


def download_file(request, file_id):
    # Retrieve the analysis object by ID
    analysis = TextReader.objects.get(id=file_id)

    # Get the original file name and append "processed" to it
    original_filename = os.path.splitext(analysis.file.name)[0]  # Extract the original filename without extension
    file_extension = os.path.splitext(analysis.file.name)[1]     # Extract the original file extension
    processed_filename = f"{original_filename}_processed{file_extension}"

    # Read the original file content
    content = analysis.file.read().decode('utf-8')

    # Create a file-like object for the modified content
    output = io.StringIO()

    # Append word, line, and character analysis to the top of the file
    output.write("File Analysis:\n")
    output.write(f"Lines: {analysis.lines}\n")
    output.write(f"Words: {analysis.words}\n")
    output.write(f"Characters: {analysis.characters}\n")
    output.write("\nOriginal File Content:\n\n")

    # Append the original content
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        output.write(f"{i}: {line}\n")  # You can include line numbers or just append raw content

    # Send the modified content as an HTTP response for download
    response = HttpResponse(output.getvalue(), content_type='text/plain')

    # Set the filename as the original file name with "_processed" appended to it
    response['Content-Disposition'] = f'attachment; filename="{processed_filename}"'

    return response
