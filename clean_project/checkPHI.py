#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge) 
# to check for DICOM fields with PHI in an XNAT project - April 2020 
#
# Usage: edit input_path and run from the server where the images are stored

import pydicom
import os, sys 
import fnmatch

# ---------------------------------------------------------------------------------------------------------------------

list_phi = ['PatientID', 'PatientName','AccessionNumber', 'AcquisitionComments', 'AcquisitionContextSequence', 'AcquisitionDeviceProcessingDescription', 'AcquisitionProtocolDescription', 'ActualHumanPerformersSequence', 'AdditionalPatientHistory', 'AdmissionID', 'AdmittingDiagnosesCodeSequence', 'AdmittingDiagnosesDescription', 'Allergies', 'Arbitrary', 'AuthorObserverSequence', 'Branch​OfService', 'BurnedInAnnotation' ,'CommentsOnThePerformedProcedureStep', 'ConfidentialityConstraintOnPatientDataDescription',  'ContentCreatorName', 'ContentCreatorIdentificationCodeSequence', 'ContentSequence', 'ContrastBolusAgent', 'ContributionDescription', 'Country​Of​Residence', 'CurrentPatientLocation', 'CurveData', 'CustodialOrganizationSequence', 'DataSetTrailingPadding', 'DerivationDescription', 'DigitalSignatureUID',  'DigitalSignaturesSequence', 'DischargeDiagnosisDescription', 'DistributionAddress', 'DistributionName', 'FillerOrderNumberImagingServiceRequest',  'FrameComments', 'GraphicAnnotationSequence', 'HumanPerformerCodeSequence', 'HumanPerformerOrganization', 'IconImageSequence', 'IdentifyingComments', 'ImageComments', 'ImagePresentationComments', 'ImagingServiceRequestComments', 'Impressions', 'InstitutionAddress', 'InstitutionCodeSequence', 'InstitutionName', 'InstitutionalDepartmentName', 'InsurancePlanIdentification', 'IntendedRecipientsOfResultsIdentificationSequence', 'InterpretationApproverSequence', 'InterpretationAuthor', 'InterpretationDiagnosisDescription', 'InterpretationIDIssuer', 'InterpretationRecorder',  'InterpretationText', 'InterpretationTranscriber', 'IssuerOfAdmissionID', 'IssuerOfPatientID', 'IssuerOfServiceEpisodeID', 'MAC', 'Manufacturer', 'MedicalAlerts',  'MedicalRecordLocator', 'MilitaryRank', 'Modality', 'ModifiedAttributesSequence', 'ModifiedImageDescription', 'ModifyingDeviceID', 'ModifyingDeviceManufacturer',  'NameOfPhysiciansReadingStudy', 'NamesOfIntendedRecipientsOfResults', 'Occupation', 'OperatorIdentificationSequence', 'OperatorsName', 'OriginalAttributesSequence', 'OrderCallbackPhoneNumber', 'OrderEnteredBy', 'OrderEntererLocation', 'OtherPatientIDs', 'OtherPatientIDsSequence', 'OtherPatientNames', 'OverlayComments', 'OverlayData', 'ParticipantSequence', 'PatientAddress', 'PatientComments', 'PatientState', 'PatientTransportArrangements', 'PatientBirthDate', 'PatientBirthName',  'PatientBirthTime', 'PatientInstitutionResidence', 'PatientInsurancePlanCodeSequence', 'PatientMotherBirthName', 'PatientPrimaryLanguageCodeSequence',  'PatientPrimaryLanguageModifierCodeSequence', 'PatientReligiousPreference', 'PatientTelephoneNumbers', 'PerformedLocation', 'PerformedProcedureStepDescription',  'PerformedProcedureStepID', 'PerformingPhysicianIdentificationSequence', 'PerformingPhysicianName', 'PersonAddress', 'PersonIdentificationCodeSequence', 'PersonName', 'PersonTelephoneNumbers', 'PhysicianApprovingInterpretation', 'PhysiciansReadingStudyIdentificationSequence', 'PhysiciansOfRecord',  'PhysiciansOfRecordIdentificationSequence', 'PlacerOrderNumberImagingServiceRequest', 'PreMedication', 'ProtocolName', 'ReasonForTheImagingServiceRequest',  'ReasonForStudy', 'ReferencedDigitalSignatureSequence', 'ReferencedPatientAliasSequence', 'ReferencedPatientSequence', 'ReferencedSOPInstanceMACSequence',  'ReferringPhysicianAddress', 'ReferringPhysicianIdentificationSequence', 'ReferringPhysicianName', 'ReferringPhysicianTelephoneNumbers', 'RegionOfResidence',  'RequestAttributesSequence', 'RequestedContrastAgent', 'RequestedProcedureComments', 'RequestedProcedureDescription', 'RequestedProcedureID', 'RequestedProcedureLocation', 'RequestingPhysician', 'RequestingService', 'ResponsibleOrganization', 'ResponsiblePerson', 'ResultsComments', 'ResultsDistributionListSequence',  'ResultsIDIssuer', 'ReviewerName', 'ScheduledHumanPerformersSequence', 'ScheduledPatientInstitutionResidence', 'ScheduledPerformingPhysicianIdentificationSequence',  'ScheduledPerformingPhysicianName', 'ScheduledProcedureStepDescription', 'SeriesDescription', 'ServiceEpisodeDescription', 'ServiceEpisodeID', 'SpecialNeeds', 'StudyComments', 'StudyDescription', 'StudyID', 'StudyIDIssuer', 'TextComments', 'TextString', 'TopicAuthor', 'TopicKeywords', 'TopicSubject', 'TopicTitle', 'VerifyingObserverIdentificationCodeSequence', 'VerifyingObserverName', 'VerifyingObserverSequence', 'VerifyingOrganization', 'VisitComments']

    
# ---------------------------------------------------------------------------------------------------------------------
# Function to check for reports, screenshots, etc based on the ImageType fields

def check_reports(input_dicom):
    try:     
        data = pydicom.dcmread(input_dicom)
        #print(data.ImageType)
        try:
            image_type_0 = data.ImageType[0].lower()
            if (('derived' in image_type_0) or ('localizer' in image_type_0) or ('report' in image_type_0) or ('presentation' in image_type_0) or ('screen' in image_type_0) or ('aqnetsc' in image_type_0) or ('exam' in image_type_0) or ('protocol' in image_type_0) or ('secondary' in image_type_0) or ('other' in image_type_0)):
                print ('ATTN! %s in file %s' % (data.ImageType, input_dicom))

        except:
            print ('ATTN! No image type in %s!' %input_dicom)
            return None
        
        try:
            image_type_1 = data.ImageType[1].lower()
            if (('derived' in image_type_1) or ('localizer' in image_type_1) or ('report' in image_type_1) or ('presentation' in image_type_1) or ('screen' in image_type_1) or ('aqnetsc' in image_type_1) or ('exam' in image_type_1) or ('protocol' in image_type_1) or ('secondary' in image_type_1) or ('other' in image_type_1)):
                print ('ATTN! %s in file %s' % (data.ImageType, input_dicom))
        except:
            print ('ATTN! No second image type in %s!' %input_dicom)
            return None

        try:
            image_type_2 = data.ImageType[2].lower()
            if (('derived' in image_type_2) or ('localizer' in image_type_2) or ('report' in image_type_2) or ('presentation' in image_type_2) or ('screen' in image_type_2) or ('aqnetsc' in image_type_2) or ('exam' in image_type_2) or ('protocol' in image_type_2) or ('secondary' in image_type_2) or ('other' in image_type_2)):
                print ('ATTN! %s in file %s' % (data.ImageType, input_dicom))
        except:
            print ('ATTN! No third image type in %s!' %input_dicom)
            return None 
        
    except:
        print('No metadata for %s' % input_dicom)

# ---------------------------------------------------------------------------------------------------------------------   
# Function to check for PHI in a list of potentially PHI DICOM tags

def check_phi(metadata):
    for field in list_phi:
         try: 
            value = metadata[field].value
            if (value != ''):
                print('   - Found %s = %s' %(field, value))
         except:
             pass

# ---------------------------------------------------------------------------------------------------------------------   
# Function to check private tags

def check_private(metadata):
    for key in metadata:
        if ('Private' in key.description()):
            print(key)

# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    input_path = '/path/to/input/dicom/'

    sessions = os.listdir(input_path)

    for session in sessions:
        print('**************')
        print('Session = %s' %(session))
        session_id = session

        # Each subdirectory is a different scan i.e. session                                                                                         
        session_path = input_path + os.sep + session + os.sep + 'SCANS'
        scans = os.listdir(session_path)

        for scan in scans:
            print('  *** Scan = %s' %(scan))
            scan_path = session_path + os.sep + scan + os.sep+ 'DICOM'            
           
            n_dicom = 0
            dicom_file = ''
            
            for dirpaths, dirnames, filenames in os.walk(scan_path):
                    for filename in filenames:
                        if(not filename.endswith(".xml")):
                            n_dicom = n_dicom + 1
                            dicom_file = os.path.join(dirpaths, filename)
                            check_reports(dicom_file)
                            dicom_path = dirpaths

            # TODO - this is only useful for CT/MR, not XRay or US, add modality check to put it back
            #if (n_dicom < 10):
            #        print('ATTN!!! - check %s - it has %d files only' %(scan_path, n_dicom))

            # ATTN: This is only done in one dicom file of the scan 
            if (n_dicom > 0):        
                metadata = pydicom.dcmread(dicom_file)
                check_phi(metadata)
                check_private(metadata)
