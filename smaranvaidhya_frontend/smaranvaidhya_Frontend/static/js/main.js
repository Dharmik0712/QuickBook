$(document).ready(function() {
    register_login_events();
    getBookingDetailsFromURL();
});

function verify_user_login(selectedLoginType, userEmailId, password) {
    var request_data = {
        user_login_type: selectedLoginType,
        email: userEmailId,
        password: password
    };
    $.ajax({
        url: '/attempt_to_login_for_user',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        success: function(data) {
            console.log("DEBUG: Login response:", data);
            if (data.status === "Login Successful") {
                console.log("Login done, User ID:", data.user_id);
                sessionStorage.setItem("user_id", data.user_id);
                setTimeout(() => {
                    window.location.href = '/Homepage';
                }, 500);
            } else {
                alert("Login failed. Please check your credentials.");
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Login failed:", errorMsg, jqXhr.responseJSON);
            alert("Something went wrong. Please try again: " + (jqXhr.responseJSON?.detail || errorMsg));
        }
    });
}

function validateGmailEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
    if (!emailRegex.test(email)) {
        return { valid: false, message: "Please enter a valid Gmail address (e.g., example@gmail.com)." };
    }
    return { valid: true, message: "Email format is valid." };
}

function save_user_registration_details(request_data) {
    const emailValidation = validateGmailEmail(request_data.email);
    if (!emailValidation.valid) {
        alert(emailValidation.message);
        return;
    }
    $.ajax({
        url: '/save_user_registration_details',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        beforeSend: function() {
            console.log("DEBUG: Sending registration data:", request_data);
        },
        success: function(data) {
            console.log("DEBUG: Registration response:", data);
            alert("Registration successful!");
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Registration failed:", errorMsg, jqXhr.responseJSON);
            alert("Failed to register: " + (jqXhr.responseJSON?.detail || errorMsg));
        }
    });
}

function formatDate(dateStr) {
    let date = new Date(dateStr);
    let year = date.getFullYear();
    let month = ('0' + (date.getMonth() + 1)).slice(-2);
    let day = ('0' + date.getDate()).slice(-2);
    return `${year}-${month}-${day}`;
}

function register_login_events() {
    $(document).on("change", "#userTypeDropdown", function(e) {
        var selectedLoginType = $("#userTypeDropdown option:selected").val();
        console.log("DEBUG: Selected login type:", selectedLoginType);
    });
    $(document).on("click", "#userLoginSubmit", function(e) {
        var selectedLoginType = $("#userTypeDropdown option:selected").val();
        var userEmailId = $("#emailId").val();
        var password = $("#password").val();
        verify_user_login(selectedLoginType, userEmailId, password);
    });
    $(document).on("click", "#registrationSubmit", function(e) {
        e.preventDefault();
        var first_name = $("#userFirstName").val().trim();
        var last_name = $("#userLastName").val().trim();
        var date_of_birth = formatDate($("#dobDate").datepicker('getDate'));
        var gender = $("#userGender").val();
        var email = $("#userEmailId").val().trim();
        var phone_number = $("#userPhoneNumber").val().trim();
        var password = $("#userPassword").val();
        var confirmPassword = $("#userConfirmPassword").val();
        var state = $("#state").val().trim();
        var city = $("#city").val().trim();
        var zip_code = $("#zipCode").val().trim();
        if (password !== confirmPassword) {
            alert("Password and Confirm Password do not match. Please try again.");
            return;
        }
        var request_data = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "email": email,
            "phone_number": parseInt(phone_number),
            "password": password,
            "city": city,
            "state": state,
            "zip_code": zip_code
        };
        save_user_registration_details(request_data);
    });
    $(document).on("click", "#contactUsSubmit", function(e) {
        var full_name = $("#contactUsFullName").val();
        var email = $("#contactUsEmailId").val();
        var message = $("#contactUsMessage").val();
        var request_data = {
            "full_name": full_name,
            "email": email,
            "message": message,
        };
        post_contact_us_data(request_data);
    });
    $('#tabs li a').click(function() {
        var tab = $(this).attr('id');
        if ($(this).hasClass('inactive')) {
            $('#tabs li a').addClass('inactive');
            $(this).removeClass('inactive');
            $('.container').hide();
            $('#' + tab + 'Container').fadeIn('slow');
        }
    });
    $(document).on("click", "#backButton", function(e) {
        $("#subjectsContainer").addClass('d-none');
        $("#coursesContainer").removeClass('d-none');
        $("#backButton").addClass('d-none');
        populate_courses_data(courses_data);
    });
    $('#doctorRegistrationSubmit').on('click', function(e) {
        e.preventDefault();
        var formData = new FormData();
        formData.append('first_name', $('#doctorFirstName').val());
        formData.append('last_name', $('#doctorLastName').val());
        formData.append('date_of_birth', $('#dobDate').val());
        formData.append('gender', $('#gender').val());
        formData.append('email', $('#doctorEmailId').val());
        formData.append('phone_number', $('#doctorPhoneNumber').val());
        formData.append('state', $('#state').val());
        formData.append('city', $('#city').val());
        formData.append('zip_code', $('#zipCode').val());
        formData.append('clinic_hospital', $('#clinic-hospital').val());
        formData.append('specialist', $('#specialist').val());
        formData.append('available_from', $('#available-from').val());
        formData.append('available_to', $('#available-to').val());
        formData.append('time_per_patient', $('#time-per-patient').val());
        formData.append('max_appointments', $('#max-appointments').val());
        formData.append('highest_qualification', $('#highest-qualification').val());
        formData.append('years_of_experience', $('#years-of-experience').val());
        formData.append('in_person_fee', $('#in-person-fee').val());
        formData.append('video_fee', $('#video-fee').val());
        formData.append('phone_fee', $('#phone-fee').val());
        formData.append('emergency_availability', $('#emergency-availability').val());
        formData.append('emergency_contact', $('#emergency-contact').val());
        formData.append('hospital_clinic_address', $('#hospital-clinic-address').val());
        formData.append('upi_id', $('#upi_id').val());
        formData.append('monday', $('#monday').prop('checked') ? 1 : 0);
        formData.append('tuesday', $('#tuesday').prop('checked') ? 1 : 0);
        formData.append('wednesday', $('#wednesday').prop('checked') ? 1 : 0);
        formData.append('thursday', $('#thursday').prop('checked') ? 1 : 0);
        formData.append('friday', $('#friday').prop('checked') ? 1 : 0);
        formData.append('saturday', $('#saturday').prop('checked') ? 1 : 0);
        formData.append('sunday', $('#sunday').prop('checked') ? 1 : 0);
        formData.append('doctor_image', $('#doctor-image')[0].files[0]);
        var imageFile = $('#doctor-image')[0].files[0];
        if (imageFile) {
            var reader = new FileReader();
            reader.onload = function(e) {
                formData.append('doctor_image', e.target.result);
            };
            reader.readAsDataURL(imageFile);
        }
        $.ajax({
            url: '/post_doctor_information_data',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("DEBUG: Doctor registration response:", response);
                alert('Doctor registered successfully!');
            },
            error: function(jqXhr, textStatus, errorMsg) {
                console.error("ERROR: Doctor registration failed:", errorMsg, jqXhr.responseJSON);
                alert('There was an error while submitting the form: ' + (jqXhr.responseJSON?.detail || errorMsg));
            }
        });
    });
    $(document).on("click", "#conAppointment", function(e) {
        e.preventDefault();
        console.log("DEBUG: Confirm Appointment button clicked!");
        const appointmentDate = $("#date").val();
        const formattedDate = convertDateFormat(appointmentDate);
        var request_data = {
            "doctor_id": $("#doctor_id").val(),
            "patient_name": $("#patientName").val() || "Unknown",
            "contact_number": $("#contactNumber").val() || "0000000000",
            "gender": $("#gender").val() || "Unknown",
            "age": parseInt($("#age").val()) || 0,
            "reason_for_visit": $("#reason").val() || "Not specified",
            "pre_existing_conditions": $("#conditions").val() || "None",
            "current_medications": $("#medications").val() || "None",
            "allergies": $("#allergies").val() || "None",
            "date_of_appointment": formattedDate,
            "slot_of_appointment": $("#slot").val(),
            "mode_of_payment": $("#paymentMethod").val() || "Cash",
            "consultancytype": $("#selectedType").val(),
            "fees": parseInt($("#feeValue").val()) || 0
        };
        console.log("DEBUG: Appointment request data:", request_data);
        post_appointment_booking_data(request_data);
    });
    $(document).on("submit", "#queryForm", function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        var $form = $(this);
        if ($form.data('submitting')) return;
        $form.data('submitting', true);
        var appointment_id = $("#appointmentId").val();
        var subject = $("#subject").val();
        var query = $("#query").val();
        if (!appointment_id || !subject || !query) {
            alert("Please fill all fields");
            $form.data('submitting', false);
            return;
        }
        var request_data = {
            appointment_id: parseInt(appointment_id),
            subject: subject,
            query: query
        };
        $.ajax({
            url: '/raise_query',
            type: "POST",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(request_data),
            success: function(data) {
                console.log("DEBUG: Query response:", data);
                if (data.data === "Query raised successfully") {
                    alert("Query submitted successfully");
                    $form[0].reset();
                } else {
                    alert("Failed to submit query: " + (data.data || "Unknown error"));
                }
            },
            error: function(jqXhr, textStatus, errorMsg) {
                console.error("ERROR: Query submission failed:", errorMsg, jqXhr.responseJSON);
                alert("Failed to submit query: " + (jqXhr.responseJSON?.error || errorMsg));
            },
            complete: function() {
                $form.data('submitting', false);
            }
        });
    });
}

function post_contact_us_data(request_data) {
    $.ajax({
        url: '/post_contact_us_data',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        beforeSend: function() {
            console.log("DEBUG: Sending contact us data:", request_data);
        },
        success: function(data) {
            console.log("DEBUG: Contact us response:", data);
            alert("Message sent successfully!");
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Contact us submission failed:", errorMsg, jqXhr.responseJSON);
            alert("Failed to send message: " + (jqXhr.responseJSON?.detail || errorMsg));
        }
    });
}

let doctor_data = [];

function get_doctor_data() {
    $.ajax({
        url: '/get_doctor_data',
        type: "GET",
        contentType: "application/json",
        success: function(data) {
            console.log("DEBUG: Doctor data response:", data);
            raw_doctor_data = JSON.parse(data);
            doctor_data = JSON.parse(raw_doctor_data['data']);
            populate_doctor_data(doctor_data);
            bind_search_events();
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Fetching doctor data:", errorMsg, jqXhr.responseJSON);
            $("#doctorResults").html("<p class='text-danger text-center'>Failed to load doctors. Please try again.</p>");
        }
    });
}

function bind_search_events() {
    $("#doctorSearch").on("input", function() {
        let query = $(this).val().trim().toLowerCase();
        search_doctors(query);
    });
}

function search_doctors(query) {
    if (!query) {
        populate_doctor_data(doctor_data);
        return;
    }
    let filtered_doctors = doctor_data.filter(doctor => {
        let full_name = `${doctor.first_name} ${doctor.last_name}`.toLowerCase();
        let city = doctor.city?.toLowerCase() || '';
        let clinic_hospital = doctor.clinic_hospital?.toLowerCase() || '';
        let qualification = doctor.highest_qualification?.toLowerCase() || '';
        let experience = doctor.years_of_experience?.toString() || '';
        return (
            full_name.includes(query) ||
            city.includes(query) ||
            clinic_hospital.includes(query) ||
            qualification.includes(query) ||
            experience.includes(query)
        );
    });
    populate_doctor_data(filtered_doctors);
}

function populate_doctor_data(doctor_data) {
    let doctorHtml = ``;
    if (doctor_data.length === 0) {
        doctorHtml = "<p class='text-gray-500 text-center'>No doctors found matching your search.</p>";
    } else {
        doctor_data.forEach(row => {
            let slotsDropdownId = `slots-${row.id}`;
            let dateDropdownId = `date-${row.id}`;
            let bookButtonId = `bookappointmentbutton-${row.id}`;
            let consultationTypeDropdownId = `consultationType-${row.id}`;
            let feeDropdownId = `fee-${row.id}`;
            let workingDays = getWorkingDays(row);
            let validDates = getNextAvailableDates(workingDays, 14);
            doctorHtml += `
            <div class="doctor-card flex flex-col bg-white rounded-lg shadow-md p-4 mb-3 space-y-3">
                <div class="flex items-center space-x-4">
                    <img src="data:image/jpeg;base64,${row['doctor_image'] || ''}" 
                        alt="Dr. ${row['first_name']} ${row['last_name']}" 
                        class="w-32 h-32 rounded-full object-cover border" />
                    <div class="flex-1" style="margin-left:10px;">
                        <p class="text-xs"><strong>Doctor ID:</strong> ${row['id']}</p>
                        <h2 class="text-lg font-semibold">Dr. ${row['first_name']} ${row['last_name']}</h2>
                        <p class="text-sm text-gray-500">${row['specialist']} | ${row['years_of_experience']} yrs</p>
                        <p class="text-xs"><strong>Gender:</strong> ${row['gender']}</p>
                        <p class="text-xs"><strong>Date of Birth:</strong> ${row['date_of_birth']}</p>
                    </div>
                </div>
                <div class="text-xs" style="margin-left:10px;">
                    <p><strong>Qualification:</strong> ${row['highest_qualification']}</p>
                    <p><strong>Availability:</strong> ${row['available_from']} - ${row['available_to']}</p>
                    <p><strong>Location:</strong> ${row['city']}, ${row['state']} (${row['zip_code']})</p>
                    <p><strong>Clinic/Hospital:</strong> ${row['clinic_hospital']}</p>
                    <p><strong>Emergency:</strong> ${row['emergency_availability'] === 'yes' ? 'Available' : 'Not Available'} (📞 ${row['emergency_contact']})</p>
                </div>
                <div class="text-xs" style="margin-left:10px;">
                    <p><strong>Fees:</strong></p>
                    <ul class="list-disc pl-4">
                        <li>In-Person: ₹${row['in_person_fee']}</li>
                        <li>Video: ₹${row['video_fee']}</li>
                        <li>Phone: ₹${row['phone_fee']}</li>
                    </ul>
                </div>
                <div class="text-xs" style="margin-left:10px;">
                    <p><strong>Working Days:</strong></p>
                    <ul class="working-days-list">
                        ${row['monday'] === "1" ? "<li>Monday</li>" : ""}
                        ${row['tuesday'] === "1" ? "<li>Tuesday</li>" : ""}
                        ${row['wednesday'] === "1" ? "<li>Wednesday</li>" : ""}
                        ${row['thursday'] === "1" ? "<li>Thursday</li>" : ""}
                        ${row['friday'] === "1" ? "<li>Friday</li>" : ""}
                        ${row['saturday'] === "1" ? "<li>Saturday</li>" : ""}
                        ${row['sunday'] === "1" ? "<li>Sunday</li>" : ""}
                    </ul>
                </div>
                <div class="text-xs" style="margin-left:10px;">
                    <label for="${dateDropdownId}"><strong>Select Date:</strong></label>
                    <select id="${dateDropdownId}" class="date-dropdown w-full border p-2 rounded">
                        <option value="">Select Date</option>
                    </select>
                    <label for="${slotsDropdownId}"><strong>Select Time Slot:</strong></label>
                    <select id="${slotsDropdownId}" class="time-slot-dropdown w-full border p-2 rounded">
                        <option value="">Select Date First</option>
                    </select>
                </div>
                <div class="text-xs" style="margin-left:10px;">
                    <label for="${consultationTypeDropdownId}"><strong>Select Consultation Type:</strong></label>
                    <select id="${consultationTypeDropdownId}" class="consultation-type-dropdown w-full border p-2 rounded">
                        <option value="">Select Type</option>
                        <option value="in_person">In-Person</option>
                        <option value="video">Video</option>
                        <option value="phone">Phone</option>
                    </select>
                    <label for="${feeDropdownId}" class="mt-2"><strong>Consultation Fee:</strong></label>
                    <select id="${feeDropdownId}" class="fee-dropdown w-full border p-2 rounded" disabled>
                        <option value="">Select Consultation Type First</option>
                    </select>
                </div>
                <div class="flex flex-col items-start gap-2 mt-6" style="margin-left:10px;">
                    <a href="${row['hospital_clinic_address']}" target="_blank" 
                        class="view-map text-blue-500 text-xs underline">
                        📍 View on Map
                    </a>
                    <a href="confirmBooking?id=${row['id']}&date=&slot=&selectedType=&feeValue=" 
                        id="${bookButtonId}"
                        class="book-btn text-white bg-red-500 px-4 py-2 rounded text-center w-full">
                        Book Appointment
                    </a>
                </div>
            </div>`;
            setTimeout(() => {
                populateDropdown(dateDropdownId, validDates, 'date');
                document.getElementById(dateDropdownId).addEventListener("change", function() {
                    let selectedDate = this.value;
                    if (selectedDate) {
                        fetchBookedSlots(row.id, selectedDate, slotsDropdownId, row.available_from, row.available_to, row.time_per_patient);
                    } else {
                        populateDropdown(slotsDropdownId, [], 'time');
                    }
                    updateBookingLink(dateDropdownId, slotsDropdownId, bookButtonId, row.id, consultationTypeDropdownId, feeDropdownId);
                });
                document.getElementById(consultationTypeDropdownId).addEventListener("change", function() {
                    let selectedType = this.value;
                    let feeDropdown = document.getElementById(feeDropdownId);
                    feeDropdown.innerHTML = "";
                    feeDropdown.disabled = false;
                    let feeValue = "";
                    if (selectedType === "in_person") {
                        feeValue = row['in_person_fee'];
                    } else if (selectedType === "video") {
                        feeValue = row['video_fee'];
                    } else if (selectedType === "phone") {
                        feeValue = row['phone_fee'];
                    }
                    if (feeValue) {
                        feeDropdown.innerHTML = `<option value="${feeValue}" selected>₹${feeValue}</option>`;
                    } else {
                        feeDropdown.innerHTML = `<option value="">Select Consultation Type First</option>`;
                        feeDropdown.disabled = true;
                    }
                    updateBookingLink(dateDropdownId, slotsDropdownId, bookButtonId, row.id, consultationTypeDropdownId, feeDropdownId);
                });
                function updateBookingLink(dateDropdownId, slotsDropdownId, bookButtonId, doctorId, consultationTypeDropdownId, feeDropdownId) {
                    let selectedDate = document.getElementById(dateDropdownId).value;
                    let selectedSlot = document.getElementById(slotsDropdownId).value;
                    let selectedType = document.getElementById(consultationTypeDropdownId).value;
                    let selectedFee = document.getElementById(feeDropdownId).value;
                    let bookingLink = `confirmBooking?id=${doctorId}&date=${selectedDate}&slot=${selectedSlot}&selectedType=${selectedType}&feeValue=${selectedFee}`;
                    document.getElementById(bookButtonId).setAttribute("href", bookingLink);
                }
                document.getElementById(dateDropdownId).addEventListener("change", function() {
                    updateBookingLink(dateDropdownId, slotsDropdownId, bookButtonId, row.id, consultationTypeDropdownId, feeDropdownId);
                });
                document.getElementById(slotsDropdownId).addEventListener("change", function() {
                    updateBookingLink(dateDropdownId, slotsDropdownId, bookButtonId, row.id, consultationTypeDropdownId, feeDropdownId);
                });
            }, 100);
        });
    }
    $("#doctorResults").html(doctorHtml);
}

function fetchBookedSlots(doctorId, date, slotsDropdownId, available_from, available_to, time_per_patient) {
    $.ajax({
        url: `/get_booked_slots?doctor_id=${doctorId}&date=${date}`,
        type: "GET",
        contentType: "application/json",
        success: function(data) {
            console.log("DEBUG: Booked slots response:", data);
            let bookedSlots = data.booked_slots || []; 
            let slots = generateTimeSlots(available_from, available_to, time_per_patient, bookedSlots, date);
            populateTimeSlotDropdown(slotsDropdownId, slots);
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Fetching booked slots:", errorMsg, jqXhr.responseJSON);
            let slots = generateTimeSlots(available_from, available_to, time_per_patient, [], date);
            populateTimeSlotDropdown(slotsDropdownId, slots);
        }
    });
}

function generateTimeSlots(available_from, available_to, time_per_patient, bookedSlots = [], selectedDate) {
    let slots = [];
    let startTime = moment(available_from, "HH:mm:ss");
    let endTime = moment(available_to, "HH:mm:ss");
    let now = moment();
    let selectedDateTime = moment(selectedDate, "YYYY-MM-DD");
    let isToday = selectedDateTime.isSame(now, 'day');
    while (startTime.isBefore(endTime)) {
        let slotTime = startTime.format("HH:mm:ss");
        let slotDisplay = startTime.format("hh:mm A");
        let isBooked = bookedSlots.includes(slotTime);
        let isPast = isToday && moment(`${selectedDate} ${slotTime}`, "YYYY-MM-DD HH:mm:ss").isBefore(now);
        if (!isPast) {
            slots.push({
                value: slotTime,
                text: slotDisplay,
                disabled: isBooked,
                booked: isBooked
            });
        }
        startTime.add(time_per_patient, 'minutes');
    }
    return slots;
}

function populateTimeSlotDropdown(dropdownId, slots) {
    let dropdown = document.getElementById(dropdownId);
    dropdown.innerHTML = `<option value="">Select Time Slot</option>`;
    slots.forEach(item => {
        let option = document.createElement("option");
        option.value = item.value;
        option.textContent = item.booked ? `${item.text} (Booked)` : item.text;
        option.disabled = item.disabled;
        dropdown.appendChild(option);
    });
}

function getWorkingDays(row) {
    let days = [];
    if (row.monday === "1") days.push("Monday");
    if (row.tuesday === "1") days.push("Tuesday");
    if (row.wednesday === "1") days.push("Wednesday");
    if (row.thursday === "1") days.push("Thursday");
    if (row.friday === "1") days.push("Friday");
    if (row.saturday === "1") days.push("Saturday");
    if (row.sunday === "1") days.push("Sunday");
    return days;
}

function getNextAvailableDates(workingDays, daysAhead) {
    let validDates = [];
    let today = moment();
    for (let i = 0; i < daysAhead; i++) {
        let currentDate = today.clone().add(i, 'days');
        let dayName = currentDate.format("dddd");
        if (workingDays.includes(dayName)) {
            validDates.push({ value: currentDate.format("YYYY-MM-DD"), text: currentDate.format("DD/MM/YYYY") });
        }
    }
    return validDates;
}

function populateDropdown(dropdownId, data, type) {
    let dropdown = document.getElementById(dropdownId);
    dropdown.innerHTML = `<option value="">${type === 'date' ? 'Select Date' : 'Select Time Slot'}</option>`;
    data.forEach(item => {
        let option = document.createElement("option");
        option.value = item.value;
        option.textContent = item.text;
        dropdown.appendChild(option);
    });
}

function convertDateFormat(dateStr) {
    return moment(dateStr, "YYYY-MM-DD").format("YYYY-MM-DD");
}

function getBookingDetailsFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    let doctor_id = urlParams.get('id');
    let selectedDate = urlParams.get('date');
    let selectedSlot = urlParams.get('slot');
    let selectedConsultancy = urlParams.get('selectedType');
    let feeValue = urlParams.get('feeValue');
    if (doctor_id) $("#doctor_id").val(doctor_id);
    if (selectedDate) {
        let formattedDisplayDate = moment(selectedDate, "YYYY-MM-DD").format("DD/MM/YYYY");
        $("#displayDate").text(formattedDisplayDate);
        $("#date").val(selectedDate);
    }
    if (selectedSlot) $("#slot").val(selectedSlot);
    if (selectedConsultancy) $("#selectedType").val(selectedConsultancy);
    if (feeValue) $("#feeValue").val(feeValue);
    console.log("DEBUG: URL Params Populated:", {
        doctor_id, selectedDate, selectedSlot, selectedConsultancy, feeValue
    });
}

function get_doctor_view_data() {
    const user_id = sessionStorage.getItem("user_id"); // Assuming doctor_id is stored as user_id
    if (!user_id) {
        console.error("ERROR: No user_id found in sessionStorage for doctor view");
        $("#appointmentsContainer").html("<p class='text-danger text-center'>Please log in to view appointments.</p>");
        window.location.href = "/login";
        return;
    }
    $.ajax({
        url: `/get_doctor_view_data?doctor_id=${encodeURIComponent(user_id)}`,
        type: "GET",
        contentType: "application/json",
        success: function(data) {
            console.log("DEBUG: Doctor view response:", data);
            // Handle array directly or fallback to data.data
            const appointments = Array.isArray(data) ? data : (Array.isArray(data.data) ? data.data : []);
            populate_doctor_view_data(appointments);
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Fetching doctor view data:", textStatus, errorMsg, jqXhr.responseJSON);
            let message = "Failed to load appointments: " + (jqXhr.responseJSON?.detail || errorMsg);
            if (jqXhr.status === 401) {
                message = "Please log in to view appointments.";
                window.location.href = "/login";
            }
            $("#appointmentsContainer").html(`<p class='text-danger text-center'>${message}</p>`);
        }
    });
}

function populate_doctor_view_data(doctor_view_data) {
    function formatDate(dateStr) {
        if (!dateStr) return "N/A";
        const date = moment(dateStr, "YYYY-MM-DD");
        return date.isValid() ? date.format("DD/MM/YYYY") : "Invalid Date";
    }
    // Filter valid dates and sort
    const uniqueDates = [...new Set(doctor_view_data
        .map(apt => apt.date_of_appointment)
        .filter(date => date && moment(date, "YYYY-MM-DD").isValid()))]
        .sort((a, b) => moment(a).diff(moment(b)));
    console.log("DEBUG: Unique dates:", uniqueDates);
    // Create dropdown HTML
    const dropdownHtml = `
        <div class="date-selector mb-4">
            <label for="date-select" class="form-label fw-bold">Select Appointment Date:</label>
            <select id="date-select" class="form-select w-auto">
                <option value="" selected>Select a date</option>
                ${uniqueDates.map(date => `<option value="${date}">${formatDate(date)}</option>`).join('')}
            </select>
        </div>
    `;
    // Create table HTML
    const tableHtml = `
        <div class="table-responsive">
            <table class="table table-bordered table-striped table-hover" id="appointmentsTable">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>Patient ID</th>
                        <th>Name</th>
                        <th>Gender</th>
                        <th>Age</th>
                        <th>Time Slot</th>
                        <th>Payment</th>
                        <th>Contact</th>
                        <th>Reason</th>
                        <th>Conditions</th>
                        <th>Medications</th>
                        <th>Allergies</th>
                        <th>Prescription</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody id="appointment-table-body"></tbody>
            </table>
        </div>
        <p id="no-appointments" class="text-center mt-3 text-muted" style="display: none;">No appointments available.</p>
    `;
    $("#appointmentsContainer").html(dropdownHtml + tableHtml);
    function populateTable(selectedDate) {
        const filteredAppointments = selectedDate
            ? doctor_view_data.filter(apt => apt.date_of_appointment === selectedDate)
            : doctor_view_data;
        const tbody = $("#appointment-table-body");
        tbody.empty();
        $("#no-appointments").hide();
        if (!Array.isArray(filteredAppointments) || filteredAppointments.length === 0) {
            $("#no-appointments").text(selectedDate ? `No appointments for ${formatDate(selectedDate)}.` : "No appointments available.").show();
            return;
        }
        filteredAppointments.forEach(appointment => {
            const safeApt = {
                appointment_id: appointment.appointment_id || 'N/A',
                patient_id: appointment.patient_id || 'N/A',
                patient_name: appointment.patient_name || 'Unknown',
                gender: appointment.gender || 'N/A',
                age: appointment.age || 'N/A',
                slot_of_appointment: appointment.slot_of_appointment || 'N/A',
                mode_of_payment: appointment.mode_of_payment || 'N/A',
                contact_number: appointment.contact_number || 'N/A',
                reason_for_visit: appointment.reason_for_visit || 'Not specified',
                pre_existing_conditions: appointment.pre_existing_conditions || 'None',
                current_medications: appointment.current_medications || 'None',
                allergies: appointment.allergies || 'None',
                prescription: appointment.prescription || '',
                visited: appointment.visited || false,
                has_prescription: appointment.has_prescription || false
            };
            const visitedButton = safeApt.visited
                ? '<span class="text-success fw-bold">Visited</span>'
                : `<button onclick="openPrescriptionModal(${safeApt.appointment_id}, '${safeApt.prescription.replace(/'/g, "\\'")}', ${safeApt.visited})" class="btn btn-success btn-sm">Update Status</button>`;
            const row = `
                <tr>
                    <td>${safeApt.appointment_id}</td>
                    <td>${safeApt.patient_id}</td>
                    <td>${safeApt.patient_name}</td>
                    <td>${safeApt.gender}</td>
                    <td>${safeApt.age}</td>
                    <td>${safeApt.slot_of_appointment}</td>
                    <td>${safeApt.mode_of_payment}</td>
                    <td>${safeApt.contact_number}</td>
                    <td class="reason text-truncate" title="${safeApt.reason_for_visit}">${safeApt.reason_for_visit}</td>
                    <td class="conditions text-truncate" title="${safeApt.pre_existing_conditions}">${safeApt.pre_existing_conditions}</td>
                    <td class="medications text-truncate" title="${safeApt.current_medications}">${safeApt.current_medications}</td>
                    <td class="allergies text-truncate" title="${safeApt.allergies}">${safeApt.allergies}</td>
                    <td class="prescription">
                        <input type="file" id="prescription_${safeApt.appointment_id}" accept="image/jpeg,image/png,application/pdf" class="form-control form-control-sm d-inline-block w-auto">
                        <button onclick="uploadPrescription(${safeApt.appointment_id})" class="btn btn-primary btn-sm mt-1">
                            ${safeApt.has_prescription ? 'Re-upload' : 'Upload'}
                        </button>
                    </td>
                    <td class="visited">${visitedButton}</td>
                </tr>`;
            tbody.append(row);
        });
    }
    const today = moment().format("YYYY-MM-DD");
    const defaultDate = uniqueDates.includes(today) ? today : uniqueDates[0] || "";
    if (defaultDate) {
        $("#date-select").val(defaultDate);
        populateTable(defaultDate);
    } else {
        $("#no-appointments").text("No appointments available.").show();
    }
    $("#date-select").on("change", function() {
        const selectedDate = $(this).val();
        populateTable(selectedDate);
    });
}
function markAppointmentVisited(appointmentId) {
    if (!confirm("Mark this appointment as visited? This cannot be undone.")) return;
    console.log(`DEBUG: Marking appointment_id=${appointmentId} as visited`);
    $.ajax({
        url: `/mark_appointment_visited/${appointmentId}`,
        type: "POST",
        contentType: "application/json",
        success: function(data) {
            console.log("DEBUG: Mark visited response:", data);
            if (data.data === "Appointment marked as visited") {
                alert("Appointment marked as visited");
                get_doctor_view_data();
            } else {
                alert("Failed to mark appointment: " + (data.data || "Unknown error"));
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Marking appointment visited:", errorMsg, jqXhr.responseJSON);
            alert("Failed to mark appointment: " + (jqXhr.responseJSON?.detail || errorMsg));
        }
    });
}

function openPrescriptionModal(appointmentId, currentPrescription, visited) {
    // Remove existing modal to prevent duplicates
    $("#prescriptionModal").remove();

    // Normalize visited to boolean
    const isVisited = visited === true || visited === "true" || visited === 1;

    // Create modal HTML
    const modalHtml = `
        <div class="modal fade" id="prescriptionModal" tabindex="-1" aria-labelledby="prescriptionModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="prescriptionModalLabel">Update Prescription and Status</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="prescriptionText" class="form-label">Prescription</label>
                            <textarea id="prescriptionText" class="form-control" rows="5">${currentPrescription || ''}</textarea>
                        </div>
                        <div class="mb-3 form-check">
                            <input type="checkbox" class="form-check-input" id="visitedCheckbox" ${isVisited ? 'checked' : ''}>
                            <label for="visitedCheckbox" class="form-check-label">Mark as Visited</label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" onclick="savePrescription(${appointmentId})">Save</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Append and initialize modal
    $("body").append(modalHtml);
    const modalElement = $("#prescriptionModal");
    if (!modalElement.length) {
        console.error("ERROR: Failed to append prescription modal to DOM");
        alert("Failed to open modal. Please try again.");
        return;
    }

    try {
        const modal = new bootstrap.Modal(modalElement[0], {
            backdrop: 'static',
            keyboard: true
        });
        modal.show();

        // Clean up modal on hide
        modalElement.on('hidden.bs.modal', function() {
            modalElement.remove();
            modal.dispose();
        });
    } catch (e) {
        console.error("ERROR: Failed to initialize Bootstrap modal:", e);
        alert("Failed to initialize modal. Please try again.");
    }
}

function savePrescription(appointmentId) {
    const prescription = $("#prescriptionText").val().trim();
    const visited = $("#visitedCheckbox").is(":checked");

    // Log the visited value for debugging
    console.log("DEBUG: Visited checkbox value:", visited, typeof visited);

    // Update visited status
    const visitedRequest = {
        visited: visited
    };
    console.log("DEBUG: Saving visited status:", { appointmentId, visitedRequest });

    $.ajax({
        url: `/mark_appointment_visited/${appointmentId}`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(visitedRequest),
        success: function(response) {
            console.log("DEBUG: Mark appointment visited response:", response);
            if (response.data === "Appointment visited status updated successfully") {
                // Update prescription text (if changed)
                if (prescription) {
                    updatePrescriptionText(appointmentId, prescription);
                } else {
                    alert("Visited status updated successfully");
                    $("#prescriptionModal").modal('hide');
                    get_doctor_view_data();
                }
            } else {
                console.error("ERROR: Unexpected response:", response);
                alert("Failed to update visited status: " + (response.data || response.error || "Unknown error"));
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Updating visited status:", textStatus, errorMsg, jqXhr.responseJSON);
            let errorDetail = jqXhr.responseJSON?.detail || jqXhr.responseJSON?.error || errorMsg || "Unknown error";
            if (jqXhr.status === 422) {
                // Extract FastAPI validation error details
                const validationErrors = jqXhr.responseJSON?.detail || [];
                errorDetail = validationErrors.length > 0 
                    ? validationErrors.map(err => `${err.loc.join('.')} - ${err.msg}`).join('; ')
                    : "Invalid request data. Please try again.";
            } else if (jqXhr.status === 404) {
                errorDetail = "Appointment not found.";
            } else if (jqXhr.status === 500) {
                errorDetail = "Server error. Please try again later.";
            }
            alert("Failed to update visited status: " + errorDetail);
        }
    });
}
// function updatePrescriptionText(appointmentId, prescription) {
//     console.log("DEBUG: Prescription text value:", prescription, typeof prescription);
//     const prescriptionRequest = {
//         prescription: prescription
//     };
//     console.log("DEBUG: Saving prescription text:", { appointmentId, prescriptionRequest });
//     $.ajax({
//         url: `/update_prescription_text/${appointmentId}`,
//         type: 'POST',
//         contentType: 'application/json',
//         data: JSON.stringify(prescriptionRequest),
//         success: function(response) {
//             console.log("DEBUG: Update prescription text response:", response);
//             if (response.data === "Prescription updated successfully") {
//                 console.log("DEBUG: Prescription update successful, refreshing table");
//                 alert("Visited status and prescription updated successfully");
//                 $("#prescriptionModal").modal('hide');
//                 get_doctor_view_data();
//             } else {
//                 console.error("ERROR: Unexpected prescription response:", response);
//                 alert("Failed to update prescription: " + (response.data || response.error || "Unknown error"));
//             }
//         },
//         error: function(jqXhr, textStatus, errorMsg) {
//             console.error("ERROR: Updating prescription text:", textStatus, errorMsg, jqXhr.responseJSON);
//             let errorDetail = jqXhr.responseJSON?.detail || jqXhr.responseJSON?.error || errorMsg || "Unknown error";
//             if (jqXhr.status === 400) {
//                 errorDetail = jqXhr.responseJSON?.detail || "Invalid prescription text. Please try again.";
//             } else if (jqXhr.status === 404) {
//                 errorDetail = "Appointment not found.";
//             } else if (jqXhr.status === 500) {
//                 errorDetail = jqXhr.responseJSON?.detail || "Server error. Please try again later.";
//             }
//             alert("Failed to update prescription: " + errorDetail);
//         }
//     });
// }

function openPrescriptionModal(appointmentId, currentPrescription, visited) {
    // Remove existing modal to prevent duplicates
    $("#prescriptionModal").remove();

    // Normalize visited to boolean
    const isVisited = visited === true || visited === "true" || visited === 1;

    // Create modal HTML
    const modalHtml = `
        <div class="modal fade" id="prescriptionModal" tabindex="-1" aria-labelledby="prescriptionModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="prescriptionModalLabel">Update Prescription and Status</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="prescriptionText" class="form-label">Prescription</label>
                            <textarea id="prescriptionText" class="form-control" rows="5">${currentPrescription || ''}</textarea>
                        </div>
                        <div class="mb-3 form-check">
                            <input type="checkbox" class="form-check-input" id="visitedCheckbox" ${isVisited ? 'checked' : ''}>
                            <label for="visitedCheckbox" class="form-check-label">Mark as Visited</label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" onclick="savePrescription(${appointmentId})">Save</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Append modal to DOM
    $("body").append(modalHtml);
    const modalElement = $("#prescriptionModal");
    if (!modalElement.length) {
        console.error("ERROR: Failed to append prescription modal to DOM");
        alert("Failed to open modal. Please try again.");
        return;
    }

    try {
        // Initialize Bootstrap modal
        const modal = new bootstrap.Modal(modalElement[0], {
            backdrop: 'static', // Prevent closing by clicking outside
            keyboard: true // Allow closing with Esc key
        });
        modal.show();
        console.log("DEBUG: Modal initialized and shown for appointmentId:", appointmentId);

        // Debug Close button click
        modalElement.find('[data-bs-dismiss="modal"]').on('click', function() {
            console.log("DEBUG: Close button clicked, attempting to hide modal");
            try {
                modal.hide();
            } catch (e) {
                console.error("ERROR: Failed to hide modal:", e);
            }
        });

        // Clean up modal on hide
        modalElement.on('hidden.bs.modal', function() {
            console.log("DEBUG: Modal hidden, cleaning up");
            modalElement.remove();
            modal.dispose();
        });

        // Debug Esc key press
        modalElement.on('keydown', function(e) {
            if (e.key === 'Escape') {
                console.log("DEBUG: Esc key pressed, attempting to hide modal");
            }
        });
    } catch (e) {
        console.error("ERROR: Failed to initialize Bootstrap modal:", e);
        alert("Failed to initialize modal. Please try again.");
    }
}

function get_user_history() {
    const user_id = sessionStorage.getItem("user_id");
    if (!user_id) {
        console.error("ERROR: No user_id found in sessionStorage");
        $("#appointmentsTableBody").html("<tr><td colspan='15' class='text-danger text-center'>Please log in to view history.</td></tr>");
        window.location.href = "/login";
        return;
    }
    $.ajax({
        url: `/get_user_history?user_id=${encodeURIComponent(user_id)}`,
        type: "GET",
        contentType: "application/json",
        success: function(data) {
            console.log("DEBUG: User history response:", data);
            // Handle array directly or fallback to data.data if backend changes
            const appointments = Array.isArray(data) ? data : (Array.isArray(data.data) ? data.data : []);
            populate_user_history(appointments);
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Fetching user history:", textStatus, errorMsg, jqXhr.responseJSON);
            let message = "Failed to load history: " + (jqXhr.responseJSON?.detail || errorMsg);
            if (jqXhr.status === 401) {
                message = "Please log in to view your history.";
                window.location.href = "/login";
            }
            $("#appointmentsTableBody").html(`<tr><td colspan='15' class='text-danger text-center'>${message}</td></tr>`);
        }
    });
}

// function populate_user_history(data) {
//     const tableBody = $("#appointmentsTableBody");
//     tableBody.empty();
//     if (!Array.isArray(data) || data.length === 0) {
//         tableBody.append("<tr><td colspan='15' class='text-center text-muted'>No appointments found.</td></tr>");
//         return;
//     }
//     data.forEach(function(item) {
//         // Safe defaults for missing fields
//         const safeItem = {
//             appointment_id: item.appointment_id || 'N/A',
//             doctor_id: item.doctor_id || 'N/A',
//             patient_name: item.patient_name || 'Unknown',
//             gender: item.gender || 'N/A',
//             age: item.age || 'N/A',
//             date_of_appointment: item.date_of_appointment ? moment(item.date_of_appointment, "YYYY-MM-DD").format("DD/MM/YYYY") : 'N/A',
//             slot_of_appointment: item.slot_of_appointment || 'N/A',
//             mode_of_payment: item.mode_of_payment || 'N/A',
//             contact_number: item.contact_number || 'N/A',
//             reason_for_visit: item.reason_for_visit || 'Not specified',
//             pre_existing_conditions: item.pre_existing_conditions || 'None',
//             current_medications: item.current_medications || 'None',
//             allergies: item.allergies || 'None',
//             has_prescription: item.has_prescription || false,
//             visited: item.visited || false,
//             consultancytype: item.consultancytype || '',
//             fees: item.fees || 0
//         };
//         const actionButtons = safeItem.visited
//             ? '<span class="text-muted">Visited (No Actions)</span>'
//             : `
//                 <button onclick="cancelAppointment(${safeItem.appointment_id})" class="btn btn-danger btn-sm">Cancel</button>
//                 <button onclick="openRescheduleModal(${safeItem.appointment_id}, '${safeItem.doctor_id}', '${safeItem.date_of_appointment}', '${safeItem.slot_of_appointment}', '${safeItem.consultancytype}', ${safeItem.fees})" class="btn btn-warning btn-sm">Reschedule</button>
//             `;
//         const row = `
//             <tr>
//                 <td>${safeItem.appointment_id}</td>
//                 <td>${safeItem.doctor_id}</td>
//                 <td>${safeItem.patient_name}</td>
//                 <td>${safeItem.gender}</td>
//                 <td>${safeItem.age}</td>
//                 <td>${safeItem.date_of_appointment}</td>
//                 <td>${safeItem.slot_of_appointment}</td>
//                 <td>${safeItem.mode_of_payment}</td>
//                 <td>${safeItem.contact_number}</td>
//                 <td class="reason text-truncate" title="${safeItem.reason_for_visit}">${safeItem.reason_for_visit}</td>
//                 <td class="conditions text-truncate" title="${safeItem.pre_existing_conditions}">${safeItem.pre_existing_conditions}</td>
//                 <td class="medications text-truncate" title="${safeItem.current_medications}">${safeItem.current_medications}</td>
//                 <td class="allergies text-truncate" title="${safeItem.allergies}">${safeItem.allergies}</td>
//                 <td class="prescription">
//                     ${safeItem.has_prescription
//                         ? `<button onclick="downloadPrescription(${safeItem.appointment_id})" class="btn btn-primary btn-sm">Download Prescription</button>`
//                         : 'Prescription not uploaded yet'}
//                 </td>
//                 <td class="actions">${actionButtons}</td>
//             </tr>
//         `;
//         tableBody.append(row);
//     });
// }

function populate_user_history(data) {
    const tableBody = $("#appointmentsTableBody");
    tableBody.empty();
    if (!Array.isArray(data) || data.length === 0) {
        tableBody.append("<tr><td colspan='16' class='text-center text-muted'>No appointments found.</td></tr>");
        return;
    }
    data.forEach(function(item) {
        // Safe defaults for missing fields
        const safeItem = {
            appointment_id: item.appointment_id || 'N/A',
            doctor_id: item.doctor_id || 'N/A',
            patient_name: item.patient_name || 'Unknown',
            gender: item.gender || 'N/A',
            age: item.age || 'N/A',
            date_of_appointment: item.date_of_appointment ? moment(item.date_of_appointment, "YYYY-MM-DD").format("DD/MM/YYYY") : 'N/A',
            slot_of_appointment: item.slot_of_appointment || 'N/A',
            mode_of_payment: item.mode_of_payment || 'N/A',
            contact_number: item.contact_number || 'N/A',
            reason_for_visit: item.reason_for_visit || 'Not specified',
            pre_existing_conditions: item.pre_existing_conditions || 'None',
            current_medications: item.current_medications || 'None',
            allergies: item.allergies || 'None',
            prescription: item.prescription || 'None',
            has_prescription: item.has_prescription || false,
            visited: item.visited || false,
            consultancytype: item.consultancytype || '',
            fees: item.fees || 0
        };
        const actionButtons = safeItem.visited
            ? '<span class="text-muted">Visited (No Actions)</span>'
            : `
                <button onclick="cancelAppointment(${safeItem.appointment_id})" class="btn btn-danger btn-sm">Cancel</button>
                <button onclick="openRescheduleModal(${safeItem.appointment_id}, '${safeItem.doctor_id}', '${safeItem.date_of_appointment}', '${safeItem.slot_of_appointment}', '${safeItem.consultancytype}', ${safeItem.fees})" class="btn btn-warning btn-sm">Reschedule</button>
            `;
        const row = `
            <tr>
                <td>${safeItem.appointment_id}</td>
                <td>${safeItem.doctor_id}</td>
                <td>${safeItem.patient_name}</td>
                <td>${safeItem.gender}</td>
                <td>${safeItem.age}</td>
                <td>${safeItem.date_of_appointment}</td>
                <td>${safeItem.slot_of_appointment}</td>
                <td>${safeItem.mode_of_payment}</td>
                <td>${safeItem.contact_number}</td>
                <td class="reason text-truncate" title="${safeItem.reason_for_visit}">${safeItem.reason_for_visit}</td>
                <td class="conditions text-truncate" title="${safeItem.pre_existing_conditions}">${safeItem.pre_existing_conditions}</td>
                <td class="medications text-truncate" title="${safeItem.current_medications}">${safeItem.current_medications}</td>
                <td class="allergies text-truncate" title="${safeItem.allergies}">${safeItem.allergies}</td>
                <td class="prescription-text text-truncate" title="${safeItem.prescription}">${safeItem.prescription}</td>
                <td class="prescription">
                    ${safeItem.has_prescription
                        ? `<button onclick="downloadPrescription(${safeItem.appointment_id})" class="btn btn-primary btn-sm">Download Prescription</button>`
                        : 'Prescription not uploaded yet'}
                </td>
                <td class="actions">${actionButtons}</td>
            </tr>
        `;
        tableBody.append(row);
    });
}

function cancelAppointment(appointmentId) {
    if (!confirm("Are you sure you want to cancel this appointment?")) return;
    console.log(`DEBUG: Sending cancel request for appointment_id=${appointmentId}`);
    $.ajax({
        url: `/cancel_appointment/${appointmentId}`,
        type: "DELETE",
        contentType: "application/json",
        success: function(data) {
            console.log("DEBUG: Cancel response:", data);
            if (data.data === "Appointment cancelled successfully") {
                alert("Appointment cancelled successfully");
                get_user_history();
            } else {
                alert("Failed to cancel appointment: " + (data.data || "Unknown error"));
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Cancelling appointment:", errorMsg, jqXhr.responseJSON);
            alert("Failed to cancel appointment: " + (jqXhr.responseJSON?.detail || errorMsg));
        }
    });
}

function openRescheduleModal(appointmentId, doctorId, currentDate, currentSlot, currentType, currentFee) {
    let modalHtml = `
        <div class="modal fade" id="rescheduleModal" tabindex="-1" aria-labelledby="rescheduleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="rescheduleModalLabel">Reschedule Appointment</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="rescheduleDate" class="form-label">Select Date</label>
                            <select id="rescheduleDate" class="form-select" disabled>
                                <option value="">Loading dates...</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="rescheduleSlot" class="form-label">Select Time Slot</label>
                            <select id="rescheduleSlot" class="form-select" disabled>
                                <option value="">Select Date First</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="rescheduleType" class="form-label">Consultation Type</label>
                            <select id="rescheduleType" class="form-select">
                                <option value="">Select Type</option>
                                <option value="in_person" ${currentType === 'in_person' ? 'selected' : ''}>In-Person</option>
                                <option value="video" ${currentType === 'video' ? 'selected' : ''}>Video</option>
                                <option value="phone" ${currentType === 'phone' ? 'selected' : ''}>Phone</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="rescheduleFee" class="form-label">Fee</label>
                            <select id="rescheduleFee" class="form-select" disabled>
                                <option value="${currentFee}" selected>₹${currentFee}</option>
                            </select>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="rescheduleCloseBtn">Close</button>
                        <button type="button" class="btn btn-primary" onclick="rescheduleAppointment(${appointmentId}, '${doctorId}')">Save Changes</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    $("body").append(modalHtml);
    const modalElement = document.getElementById("rescheduleModal");
    if (!modalElement) {
        console.error("ERROR: Modal element #rescheduleModal not found in DOM");
        return;
    }
    let modal = new bootstrap.Modal(modalElement, {
        backdrop: true,
        keyboard: true
    });
    modal.show();
    $("#rescheduleCloseBtn").on("click", function() {
        modal.hide();
    });
    $.ajax({
        url: `/get_doctor_data?doctor_id=${doctorId}`,
        type: "GET",
        contentType: "application/json",
        dataType: "json",
        success: function(data) {
            console.log("DEBUG: Doctor data response:", data);
            let doctorData;
            try {
                if (typeof data.data === 'string') {
                    doctorData = JSON.parse(data.data);
                } else if (Array.isArray(data.data) || typeof data.data === 'object') {
                    doctorData = data.data;
                } else {
                    throw new Error("Invalid doctor data format");
                }
            } catch (e) {
                console.error("ERROR: Parsing doctor data:", e, "Raw data:", data);
                alert("Failed to parse doctor data: " + e.message);
                modal.hide();
                return;
            }
            doctorData = Array.isArray(doctorData) ? doctorData : [doctorData];
            let doctor = doctorData.find(d => String(d.id).toLowerCase() === String(doctorId).toLowerCase());
            if (!doctor) {
                console.error(`ERROR: Doctor with ID ${doctorId} not found in data:`, doctorData);
                alert("Doctor data not found");
                modal.hide();
                return;
            }
            console.log("DEBUG: Found doctor:", doctor);
            $("#rescheduleDate").prop("disabled", false);
            $("#rescheduleSlot").prop("disabled", false);
            let workingDays = getWorkingDays(doctor);
            let validDates = getNextAvailableDates(workingDays, 14);
            populateDropdown("rescheduleDate", validDates, 'date');
            let formattedCurrentDate = moment(currentDate, ["YYYY-MM-DD", "DD/MM/YYYY"], true).format("YYYY-MM-DD");
            console.log("DEBUG: Formatted currentDate:", formattedCurrentDate, "Valid dates:", validDates);
            if (formattedCurrentDate && validDates.some(d => d.value === formattedCurrentDate)) {
                $("#rescheduleDate").val(formattedCurrentDate);
                fetchBookedSlots(doctorId, formattedCurrentDate, "rescheduleSlot", doctor.available_from, doctor.available_to, doctor.time_per_patient);
            } else {
                console.warn("WARNING: Current date is not valid or not in validDates:", formattedCurrentDate);
                if (validDates.length > 0) {
                    $("#rescheduleDate").val(validDates[0].value);
                    fetchBookedSlots(doctorId, validDates[0].value, "rescheduleSlot", doctor.available_from, doctor.available_to, doctor.time_per_patient);
                }
            }
            let feeValue = "";
            if (currentType === "in_person") {
                feeValue = doctor.in_person_fee;
            } else if (currentType === "video") {
                feeValue = doctor.video_fee;
            } else if (currentType === "phone") {
                feeValue = doctor.phone_fee;
            }
            if (feeValue && String(feeValue) === String(currentFee)) {
                $("#rescheduleFee").empty().append(`<option value="${feeValue}" selected>₹${feeValue}</option>`).prop("disabled", false);
            } else {
                console.warn("WARNING: Fee mismatch or invalid currentType:", { currentType, currentFee, doctor });
                $("#rescheduleFee").empty().append(`<option value="">Select Type First</option>`).prop("disabled", true);
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Fetching doctor data:", textStatus, errorMsg, jqXhr.responseJSON);
            alert("Failed to load doctor data: " + (jqXhr.responseJSON?.error || errorMsg));
            modal.hide();
        }
    });
    $("#rescheduleDate").on("change", function() {
        let selectedDate = this.value;
        if (selectedDate) {
            $.ajax({
                url: `/get_doctor_data?doctor_id=${doctorId}`,
                type: "GET",
                contentType: "application/json",
                dataType: "json",
                success: function(data) {
                    let doctorData;
                    try {
                        doctorData = typeof data.data === 'string' ? JSON.parse(data.data) : data.data;
                        doctorData = Array.isArray(doctorData) ? doctorData : [doctorData];
                    } catch (e) {
                        console.error("ERROR: Parsing doctor data on date change:", e);
                        populateDropdown("rescheduleSlot", [], 'time');
                        return;
                    }
                    let doctor = doctorData.find(d => String(d.id).toLowerCase() === String(doctorId).toLowerCase());
                    if (doctor) {
                        fetchBookedSlots(doctorId, selectedDate, "rescheduleSlot", doctor.available_from, doctor.available_to, doctor.time_per_patient);
                    } else {
                        console.error("ERROR: Doctor not found on date change:", doctorId);
                        populateDropdown("rescheduleSlot", [], 'time');
                    }
                },
                error: function(jqXhr, textStatus, errorMsg) {
                    console.error("ERROR: Fetching doctor data on date change:", errorMsg);
                    populateDropdown("rescheduleSlot", [], 'time');
                }
            });
        } else {
            populateDropdown("rescheduleSlot", [], 'time');
        }
    });
    $("#rescheduleType").on("change", function() {
        let selectedType = this.value;
        let feeDropdown = $("#rescheduleFee");
        feeDropdown.empty().prop("disabled", false);
        if (!selectedType) {
            feeDropdown.append(`<option value="">Select Type First</option>`).prop("disabled", true);
            return;
        }
        $.ajax({
            url: `/get_doctor_data?doctor_id=${doctorId}`,
            type: "GET",
            contentType: "application/json",
            dataType: "json",
            success: function(data) {
                let doctorData;
                try {
                    doctorData = typeof data.data === 'string' ? JSON.parse(data.data) : data.data;
                    doctorData = Array.isArray(doctorData) ? doctorData : [doctorData];
                } catch (e) {
                    console.error("ERROR: Parsing doctor data for fee update:", e);
                    feeDropdown.append(`<option value="">Error loading fees</option>`).prop("disabled", true);
                    return;
                }
                let doctor = doctorData.find(d => String(d.id).toLowerCase() === String(doctorId).toLowerCase());
                if (!doctor) {
                    console.error("ERROR: Doctor not found for fee update:", doctorId);
                    feeDropdown.append(`<option value="">Error loading fees</option>`).prop("disabled", true);
                    return;
                }
                let feeValue = "";
                if (selectedType === "in_person") {
                    feeValue = doctor.in_person_fee;
                } else if (selectedType === "video") {
                    feeValue = doctor.video_fee;
                } else if (selectedType === "phone") {
                    feeValue = doctor.phone_fee;
                }
                if (feeValue) {
                    feeDropdown.append(`<option value="${feeValue}" selected>₹${feeValue}</option>`);
                } else {
                    feeDropdown.append(`<option value="">Select Type First</option>`).prop("disabled", true);
                }
            },
            error: function(jqXhr, textStatus, errorMsg) {
                console.error("ERROR: Fetching doctor fees:", errorMsg);
                feeDropdown.append(`<option value="">Error loading fees</option>`).prop("disabled", true);
            }
        });
    });
    $("#rescheduleModal").on('hidden.bs.modal', function() {
        $(this).remove();
        modal.dispose();
    });
}

function rescheduleAppointment(appointmentId, doctorId) {
    let date = $("#rescheduleDate").val();
    let slot = $("#rescheduleSlot").val();
    let consultancytype = $("#rescheduleType").val();
    let fees = $("#rescheduleFee").val();
    if (!date || !slot || !consultancytype || !fees) {
        alert("Please select all fields");
        return;
    }
    let requestData = {
        date: date,
        slot: slot,
        consultancytype: consultancytype,
        fees: parseInt(fees)
    };
    console.log(`DEBUG: Rescheduling appointment_id=${appointmentId} with data:`, requestData);
    $.ajax({
        url: `/reschedule_appointment/${appointmentId}`,
        type: "PUT",
        contentType: "application/json",
        data: JSON.stringify(requestData),
        success: function(data) {
            console.log("DEBUG: Reschedule response:", data);
            if (data.data === "Appointment rescheduled successfully") {
                alert("Appointment rescheduled successfully");
                $("#rescheduleModal").modal('hide');
                get_user_history();
            } else {
                alert("Failed to reschedule appointment: " + (data.data || "Unknown error"));
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Rescheduling appointment:", errorMsg, jqXhr.responseJSON);
            alert("Failed to reschedule appointment: " + (jqXhr.responseJSON?.error || errorMsg));
        }
    });
}

function post_appointment_booking_data(request_data) {
    console.log("DEBUG: Sending AJAX Request:", request_data);
    $.ajax({
        url: '/post_appointment_booking_data',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        beforeSend: function() {
            console.log("DEBUG: Before Send - Data:", request_data);
        },
        success: function(data) {
            console.log("DEBUG: Success Response:", data);
            if (data && data.data === 'Success') {
                console.log("DEBUG: Booking successful, redirecting to /Profile");
                window.location.href = "/Profile";
            } else {
                console.log("DEBUG: Booking failed or incomplete");
                alert("Booking failed: " + (data.data || "Unknown error"));
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Booking failed:", textStatus, errorMsg, jqXhr.responseJSON);
            alert("Failed to book appointment: " + (jqXhr.responseJSON?.detail || errorMsg));
        }
    });
}

function save_prescription(appointment_id, file_content, mime_type) {
    var formData = new FormData();
    formData.append('file', file_content);
    $.ajax({
        url: `/upload_prescription/${appointment_id}`,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            console.log("DEBUG: Prescription upload response:", data);
            if (data.data === "Prescription uploaded successfully") {
                alert("Prescription uploaded successfully");
                get_doctor_view_data();
            } else {
                alert("Failed to upload prescription: " + (data.data || "Unknown error"));
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Prescription upload failed:", errorMsg, jqXhr.responseJSON);
            alert("Failed to upload prescription: " + (jqXhr.responseJSON?.data || errorMsg));
        }
    });
}

function uploadPrescription(appointment_id) {
    var fileInput = document.getElementById(`prescription_${appointment_id}`);
    if (!fileInput.files.length) {
        alert("Please select a file to upload");
        return;
    }
    var file = fileInput.files[0];
    save_prescription(appointment_id, file, file.type);
}

function downloadPrescription(appointment_id) {
    $.ajax({
        url: `/download_prescription/${appointment_id}`,
        type: 'GET',
        xhrFields: {
            responseType: 'blob'
        },
        success: function(data, status, xhr) {
            console.log("DEBUG: Prescription download response:", status);
            var contentType = xhr.getResponseHeader('content-type');
            if (contentType === 'application/json') {
                data.text().then(function(text) {
                    var json = JSON.parse(text);
                    alert(json.data);
                });
                return;
            }
            var contentDisposition = xhr.getResponseHeader('content-disposition');
            var fileName = contentDisposition 
                ? contentDisposition.split('filename=')[1].replace(/"/g, '') 
                : `prescription_${appointment_id}.pdf`;
            var url = window.URL.createObjectURL(data);
            var a = document.createElement('a');
            a.href = url;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Prescription download failed:", textStatus, errorMsg, jqXhr.responseJSON);
            alert("Failed to download prescription: " + (jqXhr.responseJSON?.data || errorMsg));
        }
    });
}

function get_queries() {
    $.ajax({
        url: '/get_queries',
        type: 'GET',
        success: function(response) {
            console.log("DEBUG: Queries response:", response);
            if (response.data) {
                populate_queries(response.data);
            } else {
                $("#queriesTableBody tbody").html("<tr><td colspan='7' class='text-center'>No queries found</td></tr>");
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Fetching queries:", errorMsg, jqXhr.responseJSON);
            $("#queriesTableBody tbody").html("<tr><td colspan='7' class='text-center'>Error loading queries</td></tr>");
        }
    });
}

function populate_queries(data) {
    var tableBody = $("#queriesTableBody tbody");
    tableBody.empty();
    if (Array.isArray(data)) {
        data.forEach(function(item) {
            var statusText = item.status === 'solved' ? 'Query Solved' : 'Query Pending';
            var buttonClass = item.status === 'solved' ? 'status-btn solved' : 'status-btn pending';
            var newStatus = item.status === 'solved' ? 'pending' : 'solved';
            var row = `
                <tr>
                    <td>${item.query_id}</td>
                    <td>${item.user_id}</td>
                    <td>${item.appointment_id || '-'}</td>
                    <td>${item.subject}</td>
                    <td>${item.query}</td>
                    <td>${item.created_at}</td>
                    <td>
                        <button onclick="updateQueryStatus(${item.query_id}, '${newStatus}')"
                            class="${buttonClass}">
                            ${statusText}
                        </button>
                    </td>
                </tr>
            `;
            tableBody.append(row);
        });
    }
}

function updateQueryStatus(query_id, status) {
    console.log(`DEBUG: Updating query ${query_id} to status: ${status}`);
    $.ajax({
        url: `/update_query_status/${query_id}`,
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ status: status }),
        success: function(data) {
            console.log("DEBUG: Update query status response:", data);
            if (data.data === 'Query status updated successfully') {
                alert('Query status updated');
                get_queries();
            } else {
                alert('Failed to update query status: ' + (data.data || 'Unknown error'));
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Updating query status:", errorMsg, jqXhr.responseJSON);
            alert('Failed Galway City Museum to update query status: ' + (jqXhr.responseJSON?.error || errorMsg));
        }
    });
}

function get_doctor_profile() {
    var email = "{{ session['email'] | e }}";
    if (!email) {
        console.error("ERROR: No email found for doctor profile request");
        alert("Failed to load profile: User not authenticated. Please log in again.");
        return;
    }
    $.ajax({
        url: `/get_doctor_profile?email=${encodeURIComponent(email)}`,
        type: 'GET',
        contentType: 'application/json',
        success: function(data) {
            console.log("DEBUG: Doctor profile data:", data);
            populate_doctor_profile(data);
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Fetching doctor profile:", {
                status: jqXhr.status,
                statusText: jqXhr.statusText,
                responseText: jqXhr.responseText,
                textStatus: textStatus,
                errorMsg: errorMsg
            });
            let errorDetail = jqXhr.responseJSON?.detail || errorMsg || "Unknown error";
            if (jqXhr.status === 404) {
                errorDetail = "No doctor profile found. Please ensure you are registered as a doctor.";
            }
            alert("Failed to load profile: " + errorDetail);
        }
    });
}

function populate_doctor_profile(data) {
    $("#doctor_id").val(data.id || '');
    $("#first_name").val(data.first_name || '');
    $("#last_name").val(data.last_name || '');
    $("#date_of_birth").val(data.date_of_birth || '');
    $("#gender").val(data.gender || '');
    $("#email").val(data.email || '');
    $("#phone_number").val(data.phone_number || '');
    $("#state").val(data.state || '');
    $("#city").val(data.city || '');
    $("#zip_code").val(data.zip_code || '');
    $("#clinic_hospital").val(data.clinic_hospital || '');
    $("#specialist").val(data.specialist || '');
    $("#available_from").val(data.available_from || '');
    $("#available_to").val(data.available_to || '');
    $("#time_per_patient").val(data.time_per_patient || '');
    $("#max_appointments").val(data.max_appointments || '');
    $("#highest_qualification").val(data.highest_qualification || '');
    $("#years_of_experience").val(data.years_of_experience || '');
    $("#in_person_fee").val(data.in_person_fee || '');
    $("#video_fee").val(data.video_fee || '');
    $("#phone_fee").val(data.phone_fee || '');
    $("#emergency_availability").val(data.emergency_availability || '');
    $("#emergency_contact").val(data.emergency_contact || '');
    $("#hospital_clinic_address").val(data.hospital_clinic_address || '');
    $("#upi_id").val(data.upi_id || '');
    $("#doctor_image").val('');
    var days = data.available_days ? data.available_days.split(',') : [];
    $("#available_days").text(days.join(', ') || 'None');
    days.forEach(function(day) {
        $(`#available_days_edit input[value="${day}"]`).prop('checked', true);
    });
}

function update_doctor_profile() {
    var doctor_id = $("#doctor_id").val();
    if (!doctor_id) {
        alert("Doctor ID is missing!");
        return;
    }
    var available_days = [];
    $("#available_days_edit input:checked").each(function() {
        available_days.push($(this).val());
    });
    var request_data = {
        first_name: $("#first_name").val().trim(),
        last_name: $("#last_name").val().trim(),
        phone_number: $("#phone_number").val().trim(),
        state: $("#state").val().trim(),
        city: $("#city").val().trim(),
        zip_code: $("#zip_code").val().trim(),
        clinic_hospital: $("#clinic_hospital").val(),
        specialist: $("#specialist").val().trim(),
        available_days: available_days.join(','),
        available_from: $("#available_from").val(),
        available_to: $("#available_to").val(),
        time_per_appointment: parseInt($("#time_per_appointment").val()) || 0,
        max_appointments: parseInt($("#max_appointments").val()) || 0,
        highest_qualification: $("#highest_qualification").val().trim(),
        years_of_experience: parseInt($("#years_of_experience").val()) || 0,
        in_person_fee: parseInt($("#in_person_fee").val()) || 0,
        video_fee: parseInt($("#video_fee").val()) || 0,
        phone_fee: parseInt($("#phone_fee").val()) || 0,
        emergency_availability: $("#emergency_availability").val(),
        emergency_contact: $("#emergency_contact").val().trim(),
        hospital_clinic_address: $("#hospital_clinic_address").val().trim(),
        upi_id: $("#upi_id").val().trim()
    };
    console.log("DEBUG: Updating doctor profile:", request_data);
    $.ajax({
        url: `/update_doctor_profile/${doctor_id}`,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(request_data),
        dataType: 'json',
        success: function(response) {
            console.log("DEBUG: Update profile response:", response);
            alert("Profile updated successfully!");
            window.location.reload();
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("ERROR: Updating profile:", errorMsg, jqXhr.responseJSON);
            alert("Failed to update profile: " + (jqXhr.responseJSON?.detail || errorMsg));
        }
    });
}

