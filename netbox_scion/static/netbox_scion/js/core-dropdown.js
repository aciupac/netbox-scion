document.addEventListener('DOMContentLoaded', function() {
    const isdasField = document.getElementById('id_isd_as');
    const coreField = document.getElementById('id_core');
    
    if (!isdasField || !coreField) {
        return; // Not on the right form
    }
    
    function updateCoreOptions(isdasId) {
        if (!isdasId) {
            coreField.innerHTML = '<option value="">--- Select ISD-AS first ---</option>';
            coreField.disabled = true;
            return;
        }
        
        // Show loading state
        coreField.innerHTML = '<option value="">Loading cores...</option>';
        coreField.disabled = true;
        
        // Fetch cores for the selected ISD-AS
        fetch(`/api/plugins/scion/isdas-cores/?isdas_id=${isdasId}`)
            .then(response => response.json())
            .then(data => {
                coreField.innerHTML = '';
                
                if (data.cores && data.cores.length > 0) {
                    // Add empty option
                    const emptyOption = document.createElement('option');
                    emptyOption.value = '';
                    emptyOption.textContent = '--- Select Core ---';
                    coreField.appendChild(emptyOption);
                    
                    // Add core options
                    data.cores.forEach(core => {
                        const option = document.createElement('option');
                        option.value = core;
                        option.textContent = core;
                        coreField.appendChild(option);
                    });
                    
                    coreField.disabled = false;
                } else {
                    coreField.innerHTML = '<option value="">No cores available</option>';
                    coreField.disabled = true;
                }
            })
            .catch(error => {
                console.error('Error fetching cores:', error);
                coreField.innerHTML = '<option value="">Error loading cores</option>';
                coreField.disabled = true;
            });
    }
    
    // Update cores when ISD-AS selection changes
    isdasField.addEventListener('change', function() {
        updateCoreOptions(this.value);
    });
    
    // Initialize on page load if ISD-AS is already selected
    if (isdasField.value) {
        updateCoreOptions(isdasField.value);
    }
});
