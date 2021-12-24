$(
    $('#download-report-button').on('click', function(e) {
        e.preventDefault();
        
        $.notifyBar({ cssClass: "success", html: "Your request is being processed. You download will start automatically once the file is ready ...",delay: 5000});
        // see the URL Setup for where this url came from
        const url = 'export_beneficiary_data';
        $.get(url)
        .done(function pollAsyncResults(data) {
            $('#download-report-button').addClass('buttonload disabled').html('Processing');
            // bind pollAsyncResults to itself to avoid clashing with 
            // the prior get request
            context: this
            // see the URL setup for where this url came from
            const origin = window.location.origin; 
            const pollAsyncUrl = `${origin}/beneficiary/poll_async_results/${data.task_id}`
            $.get(pollAsyncUrl)
            .done(function(asyncData, status, xhr) {
                context: this
                // if the status doesn't respond with 202, that means 
                // that the task finished successfully
                if (asyncData.state === "SUCCESS") {
                // stop making get requests to pollAsyncResults
                clearTimeout(pollAsyncResults);
                $('#download-report-button').removeClass('buttonload disabled')
                $('#download-report-button').addClass('mdi mdi-download').html('')
                // to download - create an anchor element and
                // simulate a click
                const a = document.createElement('a');
                document.body.appendChild(a);
                a.style='display: none';
                a.href=asyncData.location;
                a.download=asyncData.filename;
                a.click();
                // change the button back to normal and hide the     
                // overlay
                $('#download-reports-button').text('Download')
                }
                // async task still processing
                else if (asyncData.state === "PENDING") {
                // Call the function pollAsyncResults again after 
                // waiting 0.5 seconds.
                setTimeout(function() { pollAsyncResults(data) }, 2000);
                }
                else {
                clearTimeout(pollAsyncResults);
                
                }
            })
            // see PollAsyncResultsView in View Setup. If the celery 
            // task fails, and returns a JSON blob with status_code 
            // 500, PollAsyncResultsView returns a 500 response, 
            // which would indicate that the task failed
            .fail(function(xhr, status, error) {
                // stop making get requests to pollAsyncResults
                $.notifyBar({ cssClass: "error", html: "An error occured while processing your request",delay: 5000});
                
                clearTimeout(pollAsyncResults);
                
                $('#download-report-button').removeClass('buttonload disabled');
                $('#download-icon').removeClass('fa fa-circle-o-notch fa-spin px-2').addClass('mdi mdi-download');
                // add a message, modal, or something to show the user 
                // that there was an error the error in this case 
                // would be related to the asynchronous task's
                // error message
            })
        })
        .fail(function(xhr, status, error) {
            // add a message, modal, or something to show the user 
            // that there was an error
            // The error in this case would be related to the main 
            // function that makes a request to start the async task
        })
    })
)