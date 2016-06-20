///////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) OMG Plc 2009.
// All rights reserved.  This software is protected by copyright
// law and international treaties.  No part of this software / document
// may be reproduced or distributed in any form or by any means,
// whether transiently or incidentally to some other use of this software,
// without the written permission of the copyright owner.
//
///////////////////////////////////////////////////////////////////////////////

using System;
using System.Collections.Generic;
using System.Text;
using ViconDataStreamSDK.DotNET;

namespace CSharpClient
{
    class Segment
    {
        public string Name;
        public double[] LocalEuler;
        public double[] LocalTranslation;
    }

    class Program
    {
        static string Adapt(Direction i_Direction)
        {
            switch (i_Direction)
            {
                case Direction.Forward:
                    return "Forward";
                case Direction.Backward:
                    return "Backward";
                case Direction.Left:
                    return "Left";
                case Direction.Right:
                    return "Right";
                case Direction.Up:
                    return "Up";
                case Direction.Down:
                    return "Down";
                default:
                    return "Unknown";
            }
        }

        static string Adapt(DeviceType i_DeviceType)
        {
            switch (i_DeviceType)
            {
                case DeviceType.ForcePlate:
                    return "ForcePlate";
                case DeviceType.Unknown:
                default:
                    return "Unknown";
            }
        }

        static string Adapt(Unit i_Unit)
        {
            switch (i_Unit)
            {
                case Unit.Meter:
                    return "Meter";
                case Unit.Volt:
                    return "Volt";
                case Unit.NewtonMeter:
                    return "NewtonMeter";
                case Unit.Newton:
                    return "Newton";
                case Unit.Kilogram:
                    return "Kilogram";
                case Unit.Second:
                    return "Second";
                case Unit.Ampere:
                    return "Ampere";
                case Unit.Kelvin:
                    return "Kelvin";
                case Unit.Mole:
                    return "Mole";
                case Unit.Candela:
                    return "Candela";
                case Unit.Radian:
                    return "Radian";
                case Unit.Steradian:
                    return "Steradian";
                case Unit.MeterSquared:
                    return "MeterSquared";
                case Unit.MeterCubed:
                    return "MeterCubed";
                case Unit.MeterPerSecond:
                    return "MeterPerSecond";
                case Unit.MeterPerSecondSquared:
                    return "MeterPerSecondSquared";
                case Unit.RadianPerSecond:
                    return "RadianPerSecond";
                case Unit.RadianPerSecondSquared:
                    return "RadianPerSecondSquared";
                case Unit.Hertz:
                    return "Hertz";
                case Unit.Joule:
                    return "Joule";
                case Unit.Watt:
                    return "Watt";
                case Unit.Pascal:
                    return "Pascal";
                case Unit.Lumen:
                    return "Lumen";
                case Unit.Lux:
                    return "Lux";
                case Unit.Coulomb:
                    return "Coulomb";
                case Unit.Ohm:
                    return "Ohm";
                case Unit.Farad:
                    return "Farad";
                case Unit.Weber:
                    return "Weber";
                case Unit.Tesla:
                    return "Tesla";
                case Unit.Henry:
                    return "Henry";
                case Unit.Siemens:
                    return "Siemens";
                case Unit.Becquerel:
                    return "Becquerel";
                case Unit.Gray:
                    return "Gray";
                case Unit.Sievert:
                    return "Sievert";
                case Unit.Katal:
                    return "Katal";

                case Unit.Unknown:
                default:
                    return "Unknown";
            }
        }


        static void Main(string[] args)
        {
            Dictionary<uint, Segment[]> animations = new Dictionary<uint, Segment[]>();
            double frameRate = 0;

            string storageFileName = "LocalCoordinates.txt";
            string hostName = "localhost:801";
            string subjectName = "Dan_first_mocap";

            string coordFormat = "Local EulerXYZ: ({0,-6:0.00},{1,-6:0.00},{2,-6:0.00}), Local XYZ ({3,-6:0.0},{4,-6:0.0},{5,-6:0.0})";

            if (args.Length >= 1)
            {
                subjectName = args[0];
            }
            if (args.Length >= 2)
            {
                storageFileName = args[1];
            }
            if (args.Length >= 3)
            {
                hostName = args[2];
            }

            // Make a new client
            ViconDataStreamSDK.DotNET.Client MyClient = new ViconDataStreamSDK.DotNET.Client();

            // Connect to a server
            Console.Write("Connecting to {0} ...", hostName);
            while (!MyClient.IsConnected().Connected)
            {
                // Direct connection
                MyClient.Connect(hostName);
                System.Threading.Thread.Sleep(200);
                Console.Write(".");
            }
            Console.WriteLine();

            // Enable some different data types
            MyClient.EnableSegmentData();
            MyClient.DisableDeviceData();
            MyClient.DisableMarkerData();
            MyClient.DisableUnlabeledMarkerData();

            Console.WriteLine("Segment Data Enabled: {0}", MyClient.IsSegmentDataEnabled().Enabled);

            // Set the streaming mode
            MyClient.SetStreamMode(ViconDataStreamSDK.DotNET.StreamMode.ServerPush);
           

            // Set the global up axis
            MyClient.SetAxisMapping(ViconDataStreamSDK.DotNET.Direction.Forward,
                                     ViconDataStreamSDK.DotNET.Direction.Left,
                                     ViconDataStreamSDK.DotNET.Direction.Up); // Z-up
                                                                              // MyClient.SetAxisMapping( ViconDataStreamSDK.DotNET.Direction.Forward, 
                                                                              //                          ViconDataStreamSDK.DotNET.Direction.Up, 
                                                                              //                          ViconDataStreamSDK.DotNET.Direction.Right ); // Y-up

            Output_GetAxisMapping _Output_GetAxisMapping = MyClient.GetAxisMapping();
            Console.WriteLine("Axis Mapping: X-{0} Y-{1} Z-{2}", Adapt(_Output_GetAxisMapping.XAxis),
                                                                  Adapt(_Output_GetAxisMapping.YAxis),
                                                                  Adapt(_Output_GetAxisMapping.ZAxis));

            // Discover the version number
            Output_GetVersion _Output_GetVersion = MyClient.GetVersion();
            Console.WriteLine("Version: {0}.{1}.{2}", _Output_GetVersion.Major,
                                                       _Output_GetVersion.Minor,
                                                       _Output_GetVersion.Point);
            Console.WriteLine("Press any key to finish recording animation from stream");
            
            // Loop until a key is pressed
            while (true)
            {
                // Console.KeyAvailable throws an exception if stdin is a pipe (e.g.
                // with TrackerDssdkTests.py), so we use try..catch:
                try
                {
                    if (Console.KeyAvailable)
                    {
                        break;
                    }
                }
                catch (InvalidOperationException)
                {
                }

                // Get a frame
                Console.Write("Waiting for new frame...");
                //MyClient.getv
                bool isKeyPressed = false;
                while (MyClient.GetFrame().Result != ViconDataStreamSDK.DotNET.Result.Success && !isKeyPressed)
                {
                    System.Threading.Thread.Sleep(200);
                    try
                    {
                        isKeyPressed = Console.KeyAvailable;
                    }
                    catch (InvalidOperationException)
                    {
                    }
                    
                }
                if (isKeyPressed)
                {
                    break;
                }
                Console.WriteLine("\n\n\n");

                // Get the frame number
                Output_GetFrameNumber _Output_GetFrameNumber = MyClient.GetFrameNumber();
                Console.WriteLine("Frame Number: {0}", _Output_GetFrameNumber.FrameNumber + 1);
                
                // Count the number of subjects
                uint SubjectCount = MyClient.GetSubjectCount().SubjectCount;
                if (SubjectCount == 0)
                {
                    Console.WriteLine("No subject was detected");
                    continue;
                }

                bool hasRequiredSubject = false;
                for (uint subjectIndex = 0; subjectIndex < SubjectCount; ++subjectIndex)
                {
                    if (subjectName == MyClient.GetSubjectName(subjectIndex).SubjectName)
                    {
                        hasRequiredSubject = true;
                        break;
                    }
                }

                if (!hasRequiredSubject)
                {
                    Console.WriteLine("Subject {0} wasn't detected", subjectName);
                    continue;
                }

                frameRate = MyClient.GetFrameRate().FrameRateHz;

                // Count the number of segments
                uint SegmentCount = MyClient.GetSegmentCount(subjectName).SegmentCount;
                Segment[] anim = new Segment[SegmentCount];

                for (uint SegmentIndex = 0; SegmentIndex < SegmentCount; ++SegmentIndex)
                {
                    // Get the segment name
                    string SegmentName = MyClient.GetSegmentName(subjectName, SegmentIndex).SegmentName;
                    Console.Write("Name: {0, -20}, ", SegmentName);

                    // Get the local segment translation
                    Output_GetSegmentLocalTranslation _Output_GetSegmentLocalTranslation =
                      MyClient.GetSegmentLocalTranslation(subjectName, SegmentName);

                    // Get the local segment rotation in EulerXYZ co-ordinates
                    Output_GetSegmentLocalRotationEulerXYZ localEulerXYZ =
                      MyClient.GetSegmentLocalRotationEulerXYZ(subjectName, SegmentName);

                    // Get the local segment translation
                    Output_GetSegmentLocalTranslation localTranslation =
                      MyClient.GetSegmentLocalTranslation(subjectName, SegmentName);

                    Console.WriteLine(coordFormat,
                                      localEulerXYZ.Rotation[0],
                                      localEulerXYZ.Rotation[1],
                                      localEulerXYZ.Rotation[2],
                                      localTranslation.Translation[0],
                                      localTranslation.Translation[1],
                                      localTranslation.Translation[2]);

                    Segment segment = new Segment();
                    segment.Name = SegmentName;
                    segment.LocalEuler = localEulerXYZ.Rotation;
                    segment.LocalTranslation = _Output_GetSegmentLocalTranslation.Translation;
                    anim[SegmentIndex] = segment;
                }

                uint frameId = _Output_GetFrameNumber.FrameNumber + 1;
                animations[frameId] = anim;
            }

            Console.WriteLine("\n\n\n\nSaving into {0}", storageFileName);
            System.IO.StreamWriter storageFile = new System.IO.StreamWriter(storageFileName);
            List<uint> keys = new List<uint>(animations.Keys);
            keys.Sort();

            storageFile.WriteLine(keys.Count);
            storageFile.WriteLine(frameRate);

            foreach(var frame_id in keys)
            {
                var anim = animations[frame_id];
                foreach(var segment in anim)
                {
                    storageFile.Write("{0}, {1}", frame_id, segment.Name);
                    foreach(var el in segment.LocalEuler)
                    {
                        storageFile.Write(", {0}", el);
                    }
                    foreach(var el in segment.LocalTranslation)
                    {
                        storageFile.Write(", {0}", el);
                    }
                    storageFile.WriteLine();
                }
            }

            storageFile.Close();
            
            // Disconnect and dispose
            MyClient.Disconnect();
            MyClient = null;


            Console.WriteLine("Missing frames:");

            for (int keyIndex = 1; keyIndex < keys.Count; keyIndex++)
            {
                int prevFrame = (int)keys[keyIndex - 1];
                int currFrame = (int)keys[keyIndex];

                if (currFrame - prevFrame > 1)
                {
                    for (int missingFrame = prevFrame + 1; missingFrame < currFrame; missingFrame++)
                    {
                        Console.WriteLine(missingFrame);
                    }
                }
            }

            Console.ReadLine();
        }
    }
}
